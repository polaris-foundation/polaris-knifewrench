import { Message } from "../shared/types";
import { IMessageResponse } from '../message/types';

export const REQUEST_MESSAGES = "REQUEST_MESSAGES";
export const RECEIVE_MESSAGES = "RECEIVE_MESSAGES";
export const RECEIVE_MESSAGES_ERROR = "RECEIVE_MESSAGES_ERROR";
export const SELECT_MESSAGE_ROW = "SELECT_MESSAGE_ROW";

export interface MessagesState {
  messages: typeof Message[]
  fetchingMessages: boolean
  fetchingMessagesError: any | null
}

export interface RequestMessagesAction {
  type: typeof REQUEST_MESSAGES;
  status: string;
}

export interface ReceiveMessagesAction {
  type: typeof RECEIVE_MESSAGES;
  status: string;
  messages: [IMessageResponse];
}

export interface ReceiveMessagesErrorAction {
  type: typeof RECEIVE_MESSAGES_ERROR;
  error: string;
}
