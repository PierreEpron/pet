import React from 'react';
import SignIn from "./components/SignIn";
import { BrowserRouter as Router, Route, Switch } from "react-router-dom";
import HomePage from './pages/HomePage'
import Pages2 from "./pages/Pages2"
import Pages3 from "./pages/Pages3"

function App() {
  return (
    <div className="App">
      <Router>
        <Switch>
          <Route path="/" exact component={() => <SignIn />} />
            <Route path="/HomePage" exact component={() => <HomePage />} />
            <Route path="/pages2" exact component={() => <Pages2 />} />
            <Route path="/pages3" exact component={() => <Pages3 />} />
            {/*<Route path="/pagestest" exact component={() => <PageTest />} />*/}
        </Switch>
      </Router>

    </div>
  );
}


export default App;
