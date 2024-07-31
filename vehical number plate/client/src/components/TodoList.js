import React from 'react';
import Todo from './Todo';

const TodoList = ({ todos, onDelete, onComplete }) => (
  <div>
    {todos.map(todo => (
      <Todo key={todo._id} todo={todo} onDelete={onDelete} onComplete={onComplete} />
    ))}
  </div>
);

export default TodoList;
