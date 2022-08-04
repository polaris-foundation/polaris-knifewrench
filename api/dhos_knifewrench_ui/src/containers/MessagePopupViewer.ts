import { FunctionComponent } from "react";
import { Dispatch } from "redux";
import { connect } from "react-redux";

import { KnifeWrenchAppState } from "../store/shared/types";
import MessagePopup, { TMessagePopupProps } from "../components/MessagePopup";
import { clearCurrentMessage } from "../store/message/actions";

const mapStateToProps = (store: KnifeWrenchAppState): any => ({
  currentMessageUuid: store.message.currentMessageUuid,
  fetchingMessage: store.message.fetchingMessage,
  currentMessage: store.message.currentMessage,
});

const mapDispatchToProps = (dispatch: Dispatch): any => ({
  clearCurrentMessage: () => dispatch(clearCurrentMessage()),
});

export default connect<FunctionComponent<TMessagePopupProps>>(
  mapStateToProps,
  mapDispatchToProps,
)(MessagePopup);
