import React from "react";
import { Spinner } from "reactstrap";

const Loading: React.FC = (): JSX.Element => (
  <>
    <Spinner size="sm" color="secondary" />
    Loading
  </>
);

export default Loading;
