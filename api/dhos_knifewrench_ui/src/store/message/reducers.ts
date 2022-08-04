import { Reducer } from 'redux'

import {
  MessageState,
  CLEAR_MESSAGE,
  REQUEST_MESSAGE,
  RECEIVE_MESSAGE,
  RECEIVE_MESSAGE_ERROR,
} from "./types";

import {
  SELECT_MESSAGE_ROW,
} from "../messages/types";

const initialState: MessageState = {
  currentMessageUuid: null,
  fetchingMessageError: false,
};

const reducer: Reducer<MessageState> = (state = initialState, action: any) => {
  switch (action.type) {
    case SELECT_MESSAGE_ROW:
      return {
        ...state,
        currentMessageUuid: action.row.uuid,
      };
    case CLEAR_MESSAGE:
      return {
        ...state,
        currentMessageUuid: null,
        fetchingMessage: false,
        fetchingMessageError: null,
      };
    case REQUEST_MESSAGE:
      return {
        ...state,
        currentMessage: null,
        fetchingMessage: true,
        fetchingMessageError: null,
      };
    case RECEIVE_MESSAGE:
      return {
        ...state,
        currentMessage: action.message,
        fetchingMessage: false,
        fetchingMessageError: null,
      };
    case RECEIVE_MESSAGE_ERROR:
      return {
        ...state,
        currentMessage: null,
        fetchingMessage: false,
        fetchingMessageError: action.error,
      };

    /* Boilerplate */
    default:
      return state;
  }
};

export { reducer as messageReducer };
