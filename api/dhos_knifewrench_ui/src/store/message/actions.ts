import {
  REQUEST_MESSAGE,
  RECEIVE_MESSAGE,
  RECEIVE_MESSAGE_ERROR,
  CLEAR_MESSAGE,
  RequestMessageAction,
  ReceiveMessageAction,
  ReceiveMessageErrorAction,
  ClearCurrentMessageAction,
  IMessageResponse,
} from "./types";

import { Message } from "../shared/types";

export const requestMessage = (messageUuid: string): RequestMessageAction => ({
    type: REQUEST_MESSAGE,
    messageUuid,
  });
  
  export const receiveMessage = (json: IMessageResponse): ReceiveMessageAction => ({
    type: RECEIVE_MESSAGE,
    message: new Message({
      uuid: json.uuid,
      created: json.created,
      createdBy: json.created_by,
      status: json.status,
      routingKey: json.routing_key,
      messageHeaders: json.message_headers,
      messageBody: json.message_body,
      modified: json.modified,
      modifiedBy: json.modified_by,
      }
    ),
  });
  
  export const receiveMessageError = (error: any): ReceiveMessageErrorAction => ({
    type: RECEIVE_MESSAGE_ERROR,
    error,
  });
  
  // export const fetchMessage = (messageUuid: string): any => (dispatch: Dispatch) => {
  //   dispatch(requestMessage(messageUuid));
  //   return axios
  //   .get(`http://localhost:5000/dhos/v1/amqp_message/${messageUuid}`)
  //     .then(response => response.data)
  //     .then(data => dispatch(receiveMessage(data)), error => dispatch(receiveMessageError(error)));
  // };

  export const clearCurrentMessage = (): ClearCurrentMessageAction => ({
    type: CLEAR_MESSAGE,
  });
  
