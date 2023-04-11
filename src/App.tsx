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
import Crop from './components/Crop';
import Flip from './components/Flip';
import Scale from './components/Scale';
import Rotate from './components/Rotate';
import LinearMap from './components/LinearMap';
import PowerLaw from './components/PowerLaw';
import Histogram from './components/Histogram';
import HistogramEqualization from './components/HistogramEqualization';
import NonLinearFilter from './components/NonLinearFilter';
import Convolution from './components/Convolution';
import SaltPepper from './components/SaltPepper';
import { TbPolygon, TbSalt } from 'react-icons/tb';
import Shear from './components/Shear';
import Dropdown from './components/Dropdown';
import { ImageReaderProp } from './common/types';


class App extends React.Component<{}, ImageReaderProp> {
  constructor(props: {}) {
    super(props);
    this.state = {
      url: 'uploads/missing.png',
    };
    this.setImageURL = this.setImageURL.bind(this);
  }

  componentDidMount() {
    this.setState({ url: 'uploads/missing.png' });
  }


  setImageURL = (url: string) => {
    url = url.replace('http://localhost:4720/', '');
    this.setState({ url });
  }


  render() {
    return (
      <div style={{ height: '100vh' }}>
        <ResizableColumns
          left={
          <>
            <DropdownList url={this.state.url} setImageURL={this.setImageURL} />
            <div style={{ margin: '8px' }}>
              <Dropdown title='Crop' content={<Crop url={this.state.url}/>} icon={<BiCrop size={28} />} />
              <Dropdown title='Flip' content={<Flip url={this.state.url} setImageURL={this.setImageURL}/>} icon={<MdFlip size={28} />} />
              <Dropdown title='Scale' content={<Scale url={this.state.url}/>} icon={<MdOutlinePhotoSizeSelectLarge size={28} />} />
              <Dropdown title='Rotate' content={<Rotate url={this.state.url}/>} icon={<MdOutlineRotate90DegreesCw size={28} />} />
              <Dropdown title='Linear Map' content={<LinearMap url={this.state.url}/>} icon={<AiOutlineAreaChart size={28} />} />
              <Dropdown title='Power Law Map' content={<PowerLaw url={this.state.url}/>} icon={<BsPower size={28} />} />
              <Dropdown title='Histogram' content={<Histogram url={this.state.url}/>} icon={<GiHistogram size={28} />} />
              <Dropdown title='Histogram Equalization' content={<HistogramEqualization url={this.state.url} setImageURL={this.setImageURL}/>} icon={<BiEqualizer size={28} />} />
              <Dropdown title='Convolution' content={<Convolution url={this.state.url}/>} icon={<BsGrid3X3Gap size={28} />} />
              <Dropdown title='Salt and Pepper Noise' content={<SaltPepper url={this.state.url}/>} icon={<TbSalt size={28} />} />
              <Dropdown title='Non-Linear Filter' content={<NonLinearFilter url={this.state.url}/>} icon={<IoFilterSharp size={28} />} />
              <Dropdown title='Shear' content={<Shear url={this.state.url}/>} icon={<TbPolygon size={28} />} />
            </div>
          </>
          }
          right={<ImageView url={this.state.url} />}
        />
      </div>
    );
  }
}

export default App;
