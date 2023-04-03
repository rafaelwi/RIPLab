import React from 'react';
import './App.css';

class App extends React.Component<{}, { imageURL: string }> {
  uploadInput: any;

  constructor(props: any) {
    super(props);

    this.state = {
      imageURL: 'http://localhost:4720/uploads/NOIMAGE.png',
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
      <form onSubmit={this.handleUploadImage}>
        <div>
          <input ref={(ref) => { this.uploadInput = ref; }} type="file" />
        </div>
        <div>
          <button>Upload</button>
        </div>
        <img src={this.state.imageURL} alt="img" />
      </form>
    );
  }
}

export default App;
