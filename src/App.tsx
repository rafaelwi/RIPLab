import React from 'react';
import { AiOutlineAreaChart } from 'react-icons/ai';
import { BiCrop, BiEqualizer } from 'react-icons/bi';
import { BsGrid3X3Gap, BsPower } from 'react-icons/bs';
import { GiHistogram } from 'react-icons/gi';
import { IoFilterSharp } from 'react-icons/io5';
import { MdFlip, MdOutlinePhotoSizeSelectLarge, MdOutlineRotate90DegreesCw } from 'react-icons/md';
import './App.css';
import DropdownList from './components/DropdownList';
import ResizableColumns from './components/ResizableColumns';

interface DropdownItem {
  title: string;
  content: React.ReactNode;
  icon?: React.ReactNode;
}

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

  dropdownItems: DropdownItem[] = [
    {
      title: "Crop",
      content: <p>Content for Dropdown 1</p>,
      icon: <BiCrop size={28} />
    },
    {
      title: "Flip",
      content: <div>Content for Dropdown 2</div>,
      icon: <MdFlip size={28} />
    },
    {
      title: "Scale",
      content: <div style={{ height: '500px' }}>Content for Dropdown 3</div>,
      icon: <MdOutlinePhotoSizeSelectLarge size={28} />
    },
    {
      title: "Rotate",
      content: <div>Content for Dropdown 1</div>,
      icon: <MdOutlineRotate90DegreesCw size={28} />
    },
    {
      title: "Linear Map",
      content: <div>Content for Dropdown 2</div>,
      icon: <AiOutlineAreaChart size={28} />
    },
    {
      title: "Power Law Map",
      content: <div>Content for Dropdown 3</div>,
      icon: <BsPower size={28} />
    },
    {
      title: "Histogram",
      content: <div>Content for Dropdown 1</div>,
      icon: <GiHistogram size={28} />
    },
    {
      title: "Histogram Equalization",
      content: <div>Content for Dropdown 2</div>,
      icon: <BiEqualizer size={28} />
    },
    {
      title: "Convolution",
      content: <div>Content for Dropdown 3</div>,
      icon: <BsGrid3X3Gap size={28} />
    },
    {
      title: "Non-Linear Filter",
      content: <div>Content for Dropdown 1</div>,
      icon: <IoFilterSharp size={28} />
    }
  ];

  render() {
    return (
      <div
        style={{
          height: '100vh',
        }}
      >
        <ResizableColumns
          left={<DropdownList items={this.dropdownItems} />}
          right={<h1>Hello World Right</h1>}
        />
      </div>
    );
    //   <div
    //     style={{
    //       display: 'flex',
    //       flexDirection: 'row',
    //       height: '100vh'
    //     }}>

    //     <OperationMenu
    //       buttons={[
    //         { label: 'Button 1' },
    //         { label: 'Button 2' },
    //         { label: 'Button 3' },
    //         { label: 'Button 4' },
    //         { label: 'Button 5' },
    //       ]} 
    //     />

    //     <div
    //       style={{
    //         flex: 1,
    //         padding: '16px',
    //         backgroundColor: '#5f5f5f',
    //       }}>
    //       <form onSubmit={this.handleUploadImage}>
    //         <div>
    //           <input ref={(ref) => { this.uploadInput = ref; } } type="file" />
    //         </div>
    //         <div>
    //           <button>Upload</button>
    //         </div>
    //         <img src={this.state.imageURL} alt="img" />
    //       </form>
    //     </div>

    //     <div
    //       style={{
    //         width: '10%',
    //         backgroundColor: 'lightblue'
    //       }}>
    //       <ParameterMenu/>
    //     </div>
    //   </div>    
    // );
  }
}

export default App;
