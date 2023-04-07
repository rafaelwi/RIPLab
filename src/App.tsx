import React from 'react';
import './App.css';
import OperationMenu from './components/OperationMenu';

class App extends React.Component<{}, { imageURL: string }> {
  uploadInput: any;

  constructor(props: any) {
    super(props);

    this.state = {
      imageURL: 'http://localhost:4720/uploads/missing.png',
    };

    this.handleUploadImage = this.handleUploadImage.bind(this);
  }

  handleUploadImage(ev: { preventDefault: () => void; }) {
    ev.preventDefault();
    const data = new FormData();
    data.append('file', this.uploadInput.files[0]);

    fetch('http://localhost:4720/upload', {
      method: 'POST',
      body: data,
    }).then((response) => {
      response.json().then((body) => {
        this.setState({ imageURL: body.url });
      });
    });
  }

  render() {
    return (
      <div
        style={{
          display: 'flex',
          flexDirection: 'row',
          height: '100vh'
        }}>
        
        <OperationMenu
          buttons={[
            { label: 'Button 1' },
            { label: 'Button 2' },
            { label: 'Button 3' },
            { label: 'Button 4' },
            { label: 'Button 5' },
          ]} 
        />

        <div
          style={{
            flex: 1,
            padding: '16px',
            backgroundColor: '#5f5f5f',
          }}>
          <form onSubmit={this.handleUploadImage}>
            <div>
              <input ref={(ref) => { this.uploadInput = ref; } } type="file" />
            </div>
            <div>
              <button>Upload</button>
            </div>
            <img src={this.state.imageURL} alt="img" />
          </form>
        </div>

        <div
          style={{
            width: '10%',
            backgroundColor: 'lightblue'
          }}>
        </div>
      </div>    
    );
  }
}

export default App;
