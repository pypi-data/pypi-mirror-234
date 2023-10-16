# -*- coding: utf-8 -*-
"""
@Time    : 2022/7/28
@Author  : hao.wu
"""

from traitlets.config.configurable import LoggingConfigurable
from traitlets import Instance
import sqlite3
from tornado import gen, web
import uuid
from ipython_genutils.py3compat import unicode_type

from snb_node.tools.utils import maybe_future
from snb_node.tools.traittypes import InstanceFromClasses


class SessionManager(LoggingConfigurable):
    kernel_manager = Instance('snb_node.kernels.kernelmanager.MappingKernelManager')
    contents_manager = InstanceFromClasses(
        klasses=[
            'snb_node.contents.manager.ContentsManager',
            # To make custom ContentsManagers both forward+backward
            # compatible, we'll relax the strictness of this trait
            # and allow jupyter_server contents managers to pass
            # through. If jupyter_server is not installed, this class
            # will be ignored.
            'jupyter_server.snb_node.contents.manager.ContentsManager'
        ]
    )

    # session数据库初始化
    _cursor = None
    _connection = None
    _columns = {'session_id', 'path', 'name', 'type', 'kernel_id'}

    @property
    def cursor(self):
        """
        desc: 启动一个游标并创建一个名为“session”的表
        :return:
        """
        if self._cursor is None:
            self._cursor = self.connection.cursor()
            self._cursor.execute("""
                CREATE TABLE session
                    (session_id, path, name, type, kernel_id)
            """)
        return self._cursor

    @property
    def connection(self):
        """
        desc: 启动数据库连接
        :return:
        """
        if self._connection is None:
            self._connection = sqlite3.connect(':memory:')
            self._connection.row_factory = sqlite3.Row
        return self._connection

    def close(self):
        """
        desc: 关闭数据库连接
        :return:
        """
        if self._cursor is not None:
            self._cursor.close()
            self._cursor = None

    def __del__(self):
        """
        desc: SessionManager关闭的时候，关闭连接
        :return:
        """
        self.close()

    @gen.coroutine
    def session_exists(self, path):
        """
        desc: 检查给定名称的session是否存在
        :param path: 名称
        :return:
        """
        exists = False
        self.cursor.execute("SELECT * FROM session WHERE path=?", (path,))
        row = self.cursor.fetchone()
        if row is not None:
            """
            注意，尽管我们找到了会话记录，但相关的内核可能已被剔除或意外死亡。如果是这种情况，我们应该删除该记录，从而终止会话。
            这可以通过调用允许该条件的row_to_model来实现。如果row_to_model返回None，则返回false，因为此时会话已经不存在了。
            """
            model = yield maybe_future(self.row_to_model(row, tolerate_culled=True))
            if model is not None:
                exists = True
        raise gen.Return(exists)

    def new_session_id(self):
        """
        desc: 为新会话创建uuid
        :return:
        """
        return unicode_type(uuid.uuid4())

    @gen.coroutine
    def create_session(self, path=None, name=None, type=None, kernel_name=None, kernel_id=None):
        """
        desc: Creates a session and returns its model
        :param path:
        :param name:
        :param type:
        :param kernel_name:
        :param kernel_id:
        :return:
        """
        session_id = self.new_session_id()
        if kernel_id is not None and kernel_id in self.kernel_manager:
            pass
        else:
            kernel_id = yield self.start_kernel_for_session(session_id, path, name, type, kernel_name)
        result = yield maybe_future(
            self.save_session(session_id, path=path, name=name, type=type, kernel_id=kernel_id)
        )
        # py2-compat
        raise gen.Return(result)

    @gen.coroutine
    def start_kernel_for_session(self, session_id, path, name, type, kernel_name):
        """
        desc: Start a new kernel for a given session.
        :param session_id:
        :param path:
        :param name:
        :param type:
        :param kernel_name:
        :return:
        """
        # allow contents manager to specify kernels cwd
        kernel_path = self.contents_manager.get_kernel_path(path=path)
        kernel_id = yield maybe_future(
            self.kernel_manager.start_kernel(path=kernel_path, kernel_name=kernel_name)
        )
        # py2-compat
        raise gen.Return(kernel_id)

    @gen.coroutine
    def save_session(self, session_id, path=None, name=None, type=None, kernel_id=None):
        """Saves the items for the session with the given session_id

        Given a session_id (and any other of the arguments), this method
        creates a row in the sqlite session database that holds the information
        for a session.

        Parameters
        ----------
        session_id : str
            uuid for the session; this method must be given a session_id
        path : str
            the path for the given session
        name: str
            the name of the session
        type: string
            the type of the session
        kernel_id : str
            a uuid for the kernel associated with this session

        Returns
        -------
        model : dict
            a dictionary of the session model
        """
        self.cursor.execute("INSERT INTO session VALUES (?,?,?,?,?)",
                            (session_id, path, name, type, kernel_id)
                            )
        result = yield maybe_future(self.get_session(session_id=session_id))
        raise gen.Return(result)

    @gen.coroutine
    def get_session(self, **kwargs):
        """Returns the model for a particular session.

        Takes a keyword argument and searches for the value in the session
        database, then returns the rest of the session's info.

        Parameters
        ----------
        **kwargs : keyword argument
            must be given one of the keywords and values from the session database
            (i.e. session_id, path, name, type, kernel_id)

        Returns
        -------
        model : dict
            returns a dictionary that includes all the information from the
            session described by the kwarg.
        """
        if not kwargs:
            raise TypeError("must specify a column to query")

        conditions = []
        for column in kwargs.keys():
            if column not in self._columns:
                raise TypeError("No such column: %r", column)
            conditions.append(f"{column}=?")

        query = f"SELECT * FROM session WHERE {' AND '.join(conditions)}"

        self.cursor.execute(query, list(kwargs.values()))
        try:
            row = self.cursor.fetchone()
        except KeyError:
            # The kernel is missing, so the session just got deleted.
            row = None

        if row is None:
            q = []
            for key, value in kwargs.items():
                q.append(f"{key}={value!r}")

            raise web.HTTPError(404, f'Session not found: {", ".join(q)}')

        try:
            model = yield maybe_future(self.row_to_model(row))
        except KeyError as e:
            raise web.HTTPError(404, f'Session not found: {e}')
        raise gen.Return(model)

    @gen.coroutine
    def update_session(self, session_id, **kwargs):
        """Updates the values in the session database.

        Changes the values of the session with the given session_id
        with the values from the keyword arguments.

        Parameters
        ----------
        session_id : str
            a uuid that identifies a session in the sqlite3 database
        **kwargs : str
            the key must correspond to a column title in session database,
            and the value replaces the current value in the session
            with session_id.
        """
        yield maybe_future(self.get_session(session_id=session_id))

        if not kwargs:
            # no changes
            return

        sets = []
        for column in kwargs.keys():
            if column not in self._columns:
                raise TypeError(f"No such column: {column!r}")
            sets.append(f"{column}=?")
        query = f"UPDATE session SET {', '.join(sets)} WHERE session_id=?"
        self.cursor.execute(query, list(kwargs.values()) + [session_id])

    @gen.coroutine
    def list_sessions(self):
        """Returns a list of dictionaries containing all the information from
        the session database"""
        c = self.cursor.execute("SELECT * FROM session")
        result = []
        # We need to use fetchall() here, because row_to_model can delete rows,
        # which messes up the cursor if we're iterating over rows.
        for row in c.fetchall():
            try:
                model = yield maybe_future(self.row_to_model(row))
                result.append(model)
            except KeyError:
                pass
        raise gen.Return(result)

    @gen.coroutine
    def delete_session(self, session_id):
        """Deletes the row in the session database with given session_id"""
        session = yield maybe_future(self.get_session(session_id=session_id))
        yield maybe_future(self.kernel_manager.shutdown_kernel(session['kernel']['id']))
        self.cursor.execute(f"DELETE FROM session WHERE session_id=\"{session_id}\" ")

    @gen.coroutine
    def row_to_model(self, row, tolerate_culled=False):
        """
        desc: 获取sqlite数据库会话信息并将其转换为字典
        :param row:
        :param tolerate_culled:
        :return:
        """
        kernel_culled = yield maybe_future(self.kernel_culled(row['kernel_id']))
        if kernel_culled:
            """
            内核被淘汰或死亡，没有删除会话。我们不能在这里使用delete_session，因为它试图找到并关关闭内核—因此我们将直接删除行。
            如果调用者希望容忍被剔除的内核，记录一个警告并返回None。否则，用类似的方法引发KeyError消息。
            """
            self.cursor.execute(f"DELETE FROM session WHERE session_id=\"{row['session_id']}\" ")
            msg = "内核 '{kernel_id}'似乎已被删除除或意外死亡, 会话 '{session_id}' 无效. 该会话已被删除.". \
                format(kernel_id=row['kernel_id'], session_id=row['session_id'])
            if tolerate_culled:
                self.log.warning(msg + "  Continuing...")
                raise gen.Return(None)
            raise KeyError(msg)

        kernel_model = yield maybe_future(self.kernel_manager.kernel_model(row['kernel_id']))
        model = {
            'id': row['session_id'],
            'path': row['path'],
            'name': row['name'],
            'type': row['type'],
            'kernel': kernel_model
        }
        if row['type'] == 'notebook':
            # Provide the deprecated API.
            model['notebook'] = {'path': row['path'], 'name': row['name']}
        raise gen.Return(model)

    def kernel_culled(self, kernel_id):
        """
        desc: 检查内核是否仍然被认为是活动的，如果没有找到，则返回true。
        :param kernel_id:
        :return:
        """
        return kernel_id not in self.kernel_manager

