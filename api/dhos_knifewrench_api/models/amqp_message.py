from typing import Dict

from flask_batteries_included.sqldb import ModelIdentifier, db
from sqlalchemy.dialects.postgresql import JSONB


class AmqpMessage(ModelIdentifier, db.Model):
    # Pulled out key info from headers
    routing_key = db.Column(db.String, nullable=True)
    retry_queue = db.Column(db.String, nullable=True)

    # Message contents
    message_headers = db.Column(JSONB, nullable=True)
    message_body = db.Column(JSONB, nullable=True)
    message_raw_body = db.Column(db.String, nullable=True)

    # Lifecycle
    status = db.Column(db.String, nullable=True)

    def to_dict(self) -> Dict:
        return {
            "message_headers": self.message_headers,
            "message_body": self.message_body,
            "routing_key": self.routing_key,
            "status": self.status,
            **self.pack_identifier(),
        }

    def to_dict_no_body(self) -> Dict:
        return {
            "message_headers": self.message_headers,
            "routing_key": self.routing_key,
            "status": self.status,
            **self.pack_identifier(),
        }
