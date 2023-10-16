from edgedb import AsyncIOClient, errors, enums
from edgedb.asyncio_client import AsyncIOConnection # noqa
from edgedb.protocol import protocol

from deepfos import OPTION

__all__ = ['create_async_client']


class _AsyncEdgeDBConnection(AsyncIOConnection):
    async def _execute(self, execute_context) -> None:
        await self._protocol.execute(
            query=execute_context.query.query,
            args=execute_context.query.args,
            kwargs=execute_context.query.kwargs,
            reg=execute_context.cache.codecs_registry,
            qc=execute_context.cache.query_cache,
            output_format=protocol.OutputFormat.NONE,
            allow_capabilities=enums.Capability.MODIFICATIONS,
            state=(
                execute_context.state.as_dict()
                if execute_context.state else None
            ),
        )

    async def raw_query(self, query_context):
        if self.is_closed():
            await self.connect()

        reconnect = False
        capabilities = None
        i = 0
        args = dict(
            query=query_context.query.query,
            args=query_context.query.args,
            kwargs=query_context.query.kwargs,
            reg=query_context.cache.codecs_registry,
            qc=query_context.cache.query_cache,
            output_format=query_context.query_options.output_format,
            expect_one=query_context.query_options.expect_one,
            required_one=query_context.query_options.required_one,
            allow_capabilities=enums.Capability.NONE
        )
        if query_context.state is not None:
            args["state"] = query_context.state.as_dict()
        while True:
            i += 1
            try:
                if reconnect:
                    await self.connect(single_attempt=True)
                return await self._protocol.query(**args)
            except errors.EdgeDBError as e:
                if query_context.retry_options is None:
                    raise
                if not e.has_tag(errors.SHOULD_RETRY):
                    raise e
                if capabilities is None:
                    cache_item = query_context.cache.query_cache.get(
                        query_context.query.query,
                        query_context.query_options.output_format,
                        implicit_limit=0,
                        inline_typenames=False,
                        inline_typeids=False,
                        expect_one=query_context.query_options.expect_one,
                    )
                    if cache_item is not None:
                        _, _, _, capabilities = cache_item
                # A query is read-only if it has no capabilities i.e.
                # capabilities == 0. Read-only queries are safe to retry.
                # Explicit transaction conflicts as well.
                if (
                    capabilities != 0
                    and not isinstance(e, errors.TransactionConflictError)
                ):
                    raise e
                rule = query_context.retry_options.get_rule_for_exception(e)
                if i >= rule.attempts:
                    raise e
                await self.sleep(rule.backoff(i))
                reconnect = self.is_closed()


# All deprecated space in v3dev & v3test & alpha
deprecated_space = [
    'ulqtqb',
    'zauoyn',
    'ocixjo',
    'kqgboa',
    'xnthjj',
    'itarfd',
    'thugts',
    'atadqj',
    'cfzqdn',
    'bwpxhl',
    'znjcye',
    'chhwqs',
    'zguhhs',
    'svaakp',
]


def create_async_client(default_module=None):
    space = OPTION.api.header['space']
    dbname = None if space in deprecated_space else f"deepmodel_space{space}"
    cli = AsyncIOClient(
        connection_class=_AsyncEdgeDBConnection,
        max_concurrency=None,
        dsn=OPTION.edgedb.dsn,
        database=dbname,
        tls_security='insecure',
        wait_until_available=30,
        timeout=OPTION.edgedb.timeout,
    )
    if default_module:
        cli = cli.with_default_module(default_module)
    return cli
