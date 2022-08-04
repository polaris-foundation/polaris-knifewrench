import * as React from "react";
import { Navbar, NavbarBrand } from "reactstrap";

import "react-bootstrap-table-next/dist/react-bootstrap-table2.min.css";

import MessageTableViewer from "./containers/MessageTableViewer";
import MessagePopupViewer from "./containers/MessagePopupViewer";


const App: React.FC = () => (
  <>
    <MessagePopupViewer />
    <Navbar color="inverse" light expand="md">
      <NavbarBrand href="/">knife wrench manager</NavbarBrand>
    </Navbar>
    <div className="container-fluid">
      <img alt="" src="https://nerdymindsmagazine.files.wordpress.com/2013/09/knife-wrench.gif" />
    </div>
    <div id="content" className="container-fluid">
      <MessageTableViewer />
    </div>
  </>
);

export default App;
