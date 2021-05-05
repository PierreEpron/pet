import React from 'react';
import Header from "./components/Header";
import SignIn from "./components/SignIn";
import { BrowserRouter as Router, Route, Switch } from "react-router-dom";


function App() {
  return (
    <div className="App">
      <Router>
        <Switch>
          <Route path="/" exact component={() => <SignIn />} />
          <Route path="/Header" exact component={() => <Header />} />
        </Switch>
      </Router>
    </div>
  );
}


export default App;
