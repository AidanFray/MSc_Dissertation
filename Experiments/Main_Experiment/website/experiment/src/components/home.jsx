import React from 'react';
import Device from "react-device-frame";
import SplitterLayout from 'react-splitter-layout';

import 'react-splitter-layout/lib/index.css';

function Home() {
    return (
        <SplitterLayout>
            <div>
                <Device name="iphone-8" color='black' url="http://localhost:3000/image" />
            </div>
            <div>
                Pane 2
            </div>
        </SplitterLayout>
    );
}
  
export default Home;