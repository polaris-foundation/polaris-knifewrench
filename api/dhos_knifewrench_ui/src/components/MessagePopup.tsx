import axios from "axios";
import * as React from "react";
import { Button, Modal, ModalHeader, ModalBody, ModalFooter } from "reactstrap";
import { toClipboard } from "copee";
import Octicon, { Clippy } from "@primer/octicons-react";
import Loading from "./Loading";
import { IMessageResponse } from "../store/message/types";

interface ICopyProps {
  content: string;
}

const Copy: React.FC<ICopyProps> = ({ content }: ICopyProps): JSX.Element => {
  const copy = () => {
    toClipboard(content);
  };

  return (
    <span onClick={copy} role="button" onKeyPress={copy} tabIndex={0} style={{ marginLeft: "3px", cursor: "pointer" }}>
      <Octicon icon={Clippy} ariaLabel="Copy to clipboard" />
    </span>
  );
};

interface IMessagePopupItemProps {
  name: string;
  content: string;
}

const MessagePopupItem: React.FC<IMessagePopupItemProps> = ({ name, content }: IMessagePopupItemProps): JSX.Element => (
  <div className=".mt-5">
    <div>
      <strong>{name}</strong>
      <Copy content={content} />
    </div>
    <pre>{content}</pre>
  </div>
);

export type TMessagePopupProps = {
  currentMessageUuid?: string | null;
  clearCurrentMessage?: any;
};

function MessagePopup({ currentMessageUuid, clearCurrentMessage }: TMessagePopupProps): JSX.Element {
  const modalBodyStyle = { overflow: "scroll", maxHeight: 500 };
  const showModal: boolean = currentMessageUuid !== null;

  const [currentMessage, setCurrentMessage] = React.useState<IMessageResponse | null>(null);

  React.useEffect(() => {
    if (currentMessageUuid !== null) {
      axios
        .get(`http://localhost:5000/dhos/v1/amqp_message/${currentMessageUuid}`)
        .then(response => response.data)
        .then(response => {
          setCurrentMessage(response);
        });
    } else {
      setCurrentMessage(null);
    }
  }, [currentMessageUuid]);

  /* Set the body to be Loading if the modal shouldn't show, or we're fetching a message.
       Otherwise, set the real body content */
  const body =
    currentMessage === null ? (
      <Loading />
    ) : (
      <>
        <MessagePopupItem name="uuid" content={currentMessage.uuid} />
        <MessagePopupItem name="status" content={currentMessage.status} />
        <MessagePopupItem name="routing key" content={currentMessage.routing_key} />
        <MessagePopupItem name="headers" content={JSON.stringify(currentMessage.message_headers, null, 2)} />
        <MessagePopupItem name="body" content={JSON.stringify(currentMessage.message_body, null, 2)} />
        <MessagePopupItem name="created" content={currentMessage.created} />
        <MessagePopupItem name="created by" content={currentMessage.created_by} />
        <MessagePopupItem name="modified" content={currentMessage.modified} />
        <MessagePopupItem name="modified by" content={currentMessage.modified_by} />
      </>
    );

  return (
    <Modal isOpen={showModal} toggle={clearCurrentMessage} className="modal-lg">
      <ModalHeader>Message viewer</ModalHeader>
      <ModalBody style={modalBodyStyle}>{body}</ModalBody>
      <ModalFooter>
        <Button color="secondary" onKeyPress={clearCurrentMessage} onClick={clearCurrentMessage}>
          Cancel
        </Button>
      </ModalFooter>
    </Modal>
  );
}

export default MessagePopup;
