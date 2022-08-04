import { createStore, applyMiddleware, compose, combineReducers, Reducer } from "redux";
import thunk from "redux-thunk";
import logger from "redux-logger";

import { messagesReducer } from "./messages/reducers";
import { messageReducer } from "./message/reducers";

export const rootReducer: Reducer = combineReducers({
  messages: messagesReducer,
  message: messageReducer,
});

export { rootReducer as knifeWrenchApp };

const store = createStore(
  rootReducer,
  compose(
    applyMiddleware(thunk),
    applyMiddleware(logger),
  ),
);

export { store };
