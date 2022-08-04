import axios from "axios";

import {
  REQUEST_MESSAGES,
  RECEIVE_MESSAGES,
  RECEIVE_MESSAGES_ERROR,
  SELECT_MESSAGE_ROW,
  RequestMessagesAction,
  ReceiveMessagesAction,
  ReceiveMessagesErrorAction,
} from "./types";

import { MessageStatuses } from "../shared/types";
import { Dispatch } from 'redux';
import { IMessageResponse } from '../message/types';

export const requestMessages = (status: MessageStatuses): RequestMessagesAction => ({
  type: REQUEST_MESSAGES,
  status,
});

export const receiveMessages = (status: MessageStatuses, json: [IMessageResponse]): ReceiveMessagesAction => ({
  type: RECEIVE_MESSAGES,
  status,
  messages: json,
});

export const receiveMessagesError = (error: any): ReceiveMessagesErrorAction => ({
  type: RECEIVE_MESSAGES_ERROR,
  error,
});

export const selectMessageRow = (row: IMessageResponse) => ({
  type: SELECT_MESSAGE_ROW,
  row,
});

export const fetchMessages = (status: MessageStatuses): any => (dispatch: Dispatch) => {
  dispatch(requestMessages(status));
  return axios
    .get(`http://localhost:5000/dhos/v1/amqp_message?status=${status}`)
    .then(response => response.data)
    .then(data => dispatch(receiveMessages(status, data)), error => dispatch(receiveMessagesError(error)));
};
