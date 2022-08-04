import { rootReducer } from "..";

export type KnifeWrenchAppState = ReturnType<typeof rootReducer>;

export type MessageStatuses = "new" | "resubmitted" | "archived";

export class Message {
  uuid: string;
  created: string;
  createdBy: string;
  modified: string;
  modifiedBy: string;
  status: MessageStatuses;
  routingKey: string;
  messageHeaders: string;
  messageBody: string;

  constructor(
    public message: {
      uuid: string;
      created: string;
      createdBy: string;
      modified: string;
      modifiedBy: string;
      status: MessageStatuses;
      routingKey: string;
      messageHeaders: string;
      messageBody: string;
    },
  ) {
    this.uuid = message.uuid;
    this.created = message.created;
    this.createdBy = message.createdBy;
    this.modified = message.modified;
    this.modifiedBy = message.modifiedBy;
    this.status = message.status;
    this.routingKey = message.routingKey;
    this.messageHeaders = message.messageHeaders;
    this.messageBody = message.messageBody;
  }
}
