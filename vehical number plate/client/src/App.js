import React, { useState, useEffect } from 'react';
import axios from 'axios';
import TodoList from './components/TodoList';
import AddTodo from './components/AddTodo';
import './App.css';

const App = () => {
  const [todos, setTodos] = useState([]);

  useEffect(() => {
    axios.get('http://localhost:5000/todos')
      .then(res => setTodos(res.data))
      .catch(err => console.log(err));
  }, []);

  const addTodo = (title) => {
    axios.post('http://localhost:5000/todos', { title })
      .then(res => setTodos([...todos, res.data]))
      .catch(err => console.log(err));
  };

  const deleteTodo = (id) => {
    axios.delete(`http://localhost:5000/todos/${id}`)
      .then(() => setTodos(todos.filter(todo => todo._id !== id)))
      .catch(err => console.log(err));
  };

  const completeTodo = (id) => {
    const todo = todos.find(todo => todo._id === id);
    axios.put(`http://localhost:5000/todos/${id}`, { ...todo, completed: !todo.completed })
      .then(res => setTodos(todos.map(todo => (todo._id === id ? res.data : todo))))
      .catch(err => console.log(err));
  };

  return (
    <div className="App">
      <h1>Todo App</h1>
      <AddTodo onAdd={addTodo} />
      <TodoList todos={todos} onDelete={deleteTodo} onComplete={completeTodo} />
    </div>
  );
};

export default App;
