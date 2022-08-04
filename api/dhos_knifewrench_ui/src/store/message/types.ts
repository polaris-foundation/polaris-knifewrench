import { Message, MessageStatuses } from "../shared/types";

export const REQUEST_MESSAGE = "REQUEST_MESSAGE";
export const RECEIVE_MESSAGE = "RECEIVE_MESSAGE";
export const RECEIVE_MESSAGE_ERROR = "RECEIVE_MESSAGE_ERROR";
export const CLEAR_MESSAGE = "CLEAR_MESSAGE";

export interface MessageState {
  currentMessageUuid: string | null,
  fetchingMessageError: any,
}

export interface RequestMessageAction {
  type: typeof REQUEST_MESSAGE;
  messageUuid: string;
}

export interface ReceiveMessageAction {
  type: typeof RECEIVE_MESSAGE;
  message: Message;
}

export interface ReceiveMessageErrorAction {
  type: typeof RECEIVE_MESSAGE_ERROR;
  error: string;
}

export interface ClearCurrentMessageAction {
  type: typeof CLEAR_MESSAGE;
}

export interface IMessageResponse {
  uuid: string;
  created: string;
  created_by: string;
  modified: string;
  modified_by: string;
  status: MessageStatuses;
  routing_key: string;
  message_headers: any;
  message_body: any;
}
