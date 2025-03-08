import React, { useState } from 'react';

interface IProps {
    meinCoolerText?: string;
}

export const Counter: React.FC<IProps> = ({meinCoolerText}) => {
    const [count, setCount] = useState(10);
    const lul = meinCoolerText || 'count is';
    
    return (
        <div>
        <button onClick={() => setCount((count) => count + 2)}>
            {lul} {count}
        </button>
        </div>
    );
}