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
import ImageView from './components/ImageView';
import Flip from './components/Flip';
import Scale from './components/Scale';
import Rotate from './components/Rotate';


interface DropdownItem {
  title: string;
  content: React.ReactNode;
  icon?: React.ReactNode;
}

interface EditedImage {
  url: string;
}

class App extends React.Component<{}, EditedImage> {
  constructor(props: {}) {
    super(props);
    this.state = {
      url: 'http://localhost:4720/uploads/missing.png',
    };
    this.setImageURL = this.setImageURL.bind(this);
  }



  componentDidMount() {
    this.setState({ url: 'http://localhost:4720/uploads/missing.png' });
    this.dropdownItems = [
      {
        title: "Crop",
        content: <div>Content for Dropdown 1</div>,
        icon: <BiCrop size={28} />
      },
      {
        title: "Flip",
        content: <Flip imageURL={this.state.url}/>,
        icon: <MdFlip size={28} />
      },
      {
        title: "Scale",
        content: <Scale imageURL={this.state.url}/>,
        icon: <MdOutlinePhotoSizeSelectLarge size={28} />
      },
      {
        title: "Rotate",
        content: <Rotate imageURL={this.state.url}/>,
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
  }

  dropdownItems: DropdownItem[] = []

  setImageURL = (url: string) => {
    this.setState({ url });
  }



  render() {
    return (
      <div
        style={{
          height: '100vh',
        }}
      >
        <ResizableColumns
          left={<DropdownList items={this.dropdownItems} url={this.state.url} setImageURL={this.setImageURL}/>}
          right={<ImageView imageURL={this.state.url} />}
        />
      </div>
    );
  }
}

export default App;
