import React from 'react';

const Todo = ({ todo, onDelete, onComplete }) => (
  <div>
    <span style={{ textDecoration: todo.completed ? 'line-through' : 'none' }}>
      {todo.title}
    </span>
    <button onClick={() => onComplete(todo._id)}>Complete</button>
    <button onClick={() => onDelete(todo._id)}>Delete</button>
  </div>
);

export default Todo;
