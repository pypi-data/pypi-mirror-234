.. image:: https://docs.celeryq.dev/en/latest/_images/celery-banner-small.png

|license| |wheel| |pyversion|

:Version: 1.1.5
:Web: http://celeryproject.org/
:Download: https://pypi.org/project/deepfos-celery/
:Source: https://gitee.com/python-development-team/deepfos-celery/
:Keywords: task, queue, job, async, rabbitmq, amqp, redis,
  python, distributed, actors

What is this?
=============

本项目基于 ``celery-5.0.5`` 开发，主要功能：

* 添加 ``asyncio`` 支持，更容易集成到异步web框架
* 支持 ``redis`` 集群

**注：项目是 ``celery`` 的超集，但并非所有功能都支持 ``asyncio`` ，并且目前仅完成了 ``redis`` 作为 ``broker`` 和 ``backend`` 的支持。**

Get Started
===========

创建任务和官方 ``celery`` 一样:

.. code-block:: python

    from celery import Celery

    app = Celery('hello', broker='redis://:@localhost/')

    @app.task(aio_variant=True)
    def hello():
        return 'hello world'


但增加了 ``aio_variant`` 这一参数，相较于普通的任务发送和获取结果的方式：

.. code-block:: python

    task = hello.apply_async()
    result = task.get()


可以使用:

.. code-block:: python

    task = await hello.aio.apply_async()
    result = await task.get()


**注意**

    这不只是一个简单的语法糖，而是确实使用 ``aioredis`` 替换了原有 ``redis-py`` 的同步网络请求。


.. _license:

License
=======

This software is licensed under the `New BSD License`. See the ``LICENSE``
file in the top distribution directory for the full license text.

.. # vim: syntax=rst expandtab tabstop=4 shiftwidth=4 shiftround

.. |license| image:: https://img.shields.io/pypi/l/celery.svg
    :alt: BSD License
    :target: https://opensource.org/licenses/BSD-3-Clause

.. |wheel| image:: https://img.shields.io/pypi/wheel/celery.svg
    :alt: Celery can be installed via wheel
    :target: https://pypi.org/project/celery/

.. |pyversion| image:: https://img.shields.io/pypi/pyversions/celery.svg
    :alt: Supported Python versions.
    :target: https://pypi.org/project/celery/

