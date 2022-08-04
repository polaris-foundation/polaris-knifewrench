import { Reducer } from 'redux'

import {
  REQUEST_MESSAGES,
  RECEIVE_MESSAGES,
  RECEIVE_MESSAGES_ERROR,
  MessagesState
} from "./types";

export const initialState: MessagesState = {
  messages: [],
  fetchingMessages: false,
  fetchingMessagesError: false,
}

const reducer: Reducer<MessagesState> = (state: MessagesState = initialState, action: any) => {
  switch (action.type) {
    /* Message list */
    case REQUEST_MESSAGES:
      return {
        ...state,
        messages: [],
        fetchingMessages: true,
        fetchingMessagesError: null,
      };
    case RECEIVE_MESSAGES:
      return {
        ...state,
        messages: action.messages,
        fetchingMessages: false,
        fetchingMessagesError: null,
      };
    case RECEIVE_MESSAGES_ERROR:
      return {
        ...state,
        messages: [],
        fetchingMessages: false,
        fetchingMessagesError: action.error,
      };
    default:
      return state;
  }
}

export { reducer as messagesReducer };
