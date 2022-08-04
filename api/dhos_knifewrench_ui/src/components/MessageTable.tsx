import React, { useEffect } from "react";
import BootstrapTable from "react-bootstrap-table-next";
import Loading from "./Loading";

import { Message } from "../store/shared/types";
import { IMessageResponse } from "../store/message/types";

const columns = [
  {
    dataField: "status",
    text: "status",
  },
  {
    dataField: "routing_key",
    text: "routing key",
  },
  {
    dataField: "message_headers.x-death[0].exchange",
    text: "exchange",
  },
  {
    dataField: "message_headers.x-death[0].queue",
    text: "queue",
  },
  {
    dataField: "message_headers.x-death[0].reason",
    text: "reason",
  },
  {
    dataField: "message_headers.x-death[0].time",
    text: "time",
  },
];

export type TMessageTableProps = {
  fetchingMessages?: boolean;
  messages?: [Message] | [];
  selectMessageRow?: any;
  fetchMessages?: any;
};

function MessageTable({ fetchMessages, messages, fetchingMessages, selectMessageRow }: TMessageTableProps): JSX.Element {
  useEffect(() => {
    fetchMessages();
  }, []);

  const rowEvents = {
    onClick: (e: any, row: IMessageResponse) => {
      selectMessageRow(row);
    },
  };

  if (fetchingMessages || messages === []) return <Loading />;

  return (
    <div id="content-table" style={{ margin: "0 10px" }}>
      <BootstrapTable bootstrap4 condensed hover striped bordered rowEvents={rowEvents} rowStyle={{ cursor: "pointer" }} keyField="uuid" data={messages} columns={columns} />
    </div>
  );
}

export default MessageTable;
