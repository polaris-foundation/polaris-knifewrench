import { FunctionComponent } from "react";
import { Dispatch } from "redux";
import { connect } from "react-redux";

import { KnifeWrenchAppState } from "../store/shared/types";
import MessageTable, { TMessageTableProps } from "../components/MessageTable";
import { fetchMessages, selectMessageRow } from "../store/messages/actions";

const mapStateToProps = (store: KnifeWrenchAppState): any => ({
  messages: store.messages.messages,
  fetchingMessages: store.messages.fetchingMessages,
  fetchingMessagesError: store.messages.fetchingMessagesError,
});

const mapDispatchToProps = (dispatch: Dispatch): any => ({
  fetchMessages: () => dispatch(fetchMessages("new")),
  selectMessageRow: (row: any) => dispatch(selectMessageRow(row)),
});

export default connect<FunctionComponent<TMessageTableProps>>(
  mapStateToProps,
  mapDispatchToProps,
)(MessageTable);
