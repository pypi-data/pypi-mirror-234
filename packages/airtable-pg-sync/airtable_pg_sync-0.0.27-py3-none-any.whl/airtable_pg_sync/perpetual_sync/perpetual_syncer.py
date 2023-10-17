import functools
import logging
import time

from ..core import change_handler
from ..core.clients import airtable
from ..core.types import bridges, env_types


class PerpetualSyncer:

    def __init__(self, queue: bridges.Queue):
        self.queue = queue
        self.cursors: dict[env_types.Replication, str] = {}

    @functools.cached_property
    def logger(self) -> logging.Logger:
        return logging.getLogger('Perpetual Syncer')

    def start(self):
        iterations_from_change = 0

        while True:

            if self.queue.empty:

                if iterations_from_change == 100:
                    self.logger.info('No Changes detected in the last 25s')
                    iterations_from_change = 0

                iterations_from_change += 1
                time.sleep(0.25)
                continue

            iterations_from_change = 0

            change_context = self.queue.pop()
            airtable_client = airtable.Client(base_id=change_context.replication.base_id)
            received_changes, self.cursors[change_context.replication] = airtable_client.get_changes(
                cursor=self.cursors.get(change_context.replication),
                webhook_id=change_context.id
            )

            for change in received_changes:
                change_handler.Handler(replication=change_context.replication).handle_change(change)
