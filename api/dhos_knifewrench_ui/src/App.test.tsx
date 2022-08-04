import * as React from "react";
import * as ReactDOM from "react-dom";
import { Provider } from "react-redux";
import App from "./App";
import { store } from "./store";
import moxios from "moxios";

beforeEach(function () {
  moxios.install()
})

afterEach(function () {
  moxios.uninstall()
})

it("renders without crashing", () => {
  moxios.stubRequest("http://localhost:5000/dhos/v1/amqp_message?status=new", {
    status: 200,
    responseText: "[]",
  });

  const div = document.createElement("div");
  ReactDOM.render(
    <Provider store={store}>
      <App />
    </Provider>,
    div,
  );
  ReactDOM.unmountComponentAtNode(div);
});
