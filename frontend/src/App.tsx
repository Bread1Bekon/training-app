/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { AuthProvider } from "./context/AuthContext";
import Landing from "./components/Landing";
import Login from "./components/auth/Login";
import Register from "./components/auth/Register";
import CreateForm from "./components/auth/CreateForm";
import Profile from "./components/Profile";
import Swipe from "./components/Swipe";

export default function App() {
  return (
    <AuthProvider>
      <Router>
        <Routes>
          <Route path="/" element={<Landing />} />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/create-form/:userId" element={<CreateForm />} />
          <Route path="/profile/:userId" element={<Profile />} />
          <Route path="/swipe" element={<Swipe />} />
        </Routes>
      </Router>
    </AuthProvider>
  );
}

