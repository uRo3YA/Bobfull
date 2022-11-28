import logo from "./logo.svg";
import "./App.css";
import { useState } from "react";
import axios from "axios";

function App() {
    return (
        <div className="App">
            <h1>연습</h1>
            <div>
                <button
                    onClick={() => {
                        axios.get("http://127.0.0.1:8000/articles/review/1/").then((res) => {
                            console.log(res.data);
                        });
                    }}
                >
                    버튼
                </button>
            </div>
        </div>
    );
}

export default App;
