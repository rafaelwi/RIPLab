import React from 'react';
import { AiOutlineAreaChart } from 'react-icons/ai';
import { BiCrop, BiEqualizer } from 'react-icons/bi';
import { BsGrid3X3Gap, BsPower } from 'react-icons/bs';
import { GiHistogram } from 'react-icons/gi';
import { IoFilterSharp } from 'react-icons/io5';
import { MdFlip, MdOutlinePhotoSizeSelectLarge, MdOutlineRotate90DegreesCw } from 'react-icons/md';
import { TbPolygon, TbSalt } from 'react-icons/tb';

import './App.css';

import { ImageHistoryProp } from './common/types';
import { useUndoableState } from './common/utils';

import Convolution from './components/Convolution';
import Crop from './components/Crop';
import Dropdown from './components/Dropdown';
import DropdownList from './components/DropdownList';
import Flip from './components/Flip';
import Histogram from './components/Histogram';
import HistogramEqualization from './components/HistogramEqualization';
import ImageView from './components/ImageView';
import LinearMap from './components/LinearMap';
import NonLinearFilter from './components/NonLinearFilter';
import PowerLaw from './components/PowerLaw';
import ResizableColumns from './components/ResizableColumns';
import Rotate from './components/Rotate';
import SaltPepper from './components/SaltPepper';
import Scale from './components/Scale';
import Shear from './components/Shear';


class App extends React.Component<{}, ImageHistoryProp> {
  initImg : string = 'uploads/missing.png';

  constructor(props: {}) {
    super(props);

    // Set up image view states
    this.state = {
      url: this.initImg,
      originalURL: this.initImg,
      history: [this.initImg],
      undoHistory: [],
    };

    this.setImageURL = this.setImageURL.bind(this);
    this.setOriginalURL = this.setOriginalURL.bind(this);
    this.modifyHistory = this.modifyHistory.bind(this);
  }

  
  componentDidMount() {
    this.setState({ 
      url: this.initImg, 
      originalURL: this.initImg, 
      history: [this.initImg],
      undoHistory: [], 
    });
  }

  setImageURL = (url: string) => {
    url = url.replace('http://localhost:4720/', '');
    this.setState({ url: url });
    this.modifyHistory('add', url);
  }

  setImageURLOnRedo = (url: string) => {
    url = url.replace('http://localhost:4720/', '');
    this.setState({ url: url });
    this.modifyHistory('addonredo', url);
  }

  setOriginalURL = (url: string) => {
    url = url.replace('http://localhost:4720/', '');
    this.setState({ originalURL: url });
    this.modifyHistory('add', url);
  }

  modifyHistory = (action: string, url: string) => {
    if (action === 'add') {
      url = url.replace('http://localhost:4720/', '');
      this.setState({ 
        history: [...this.state.history, url],
        undoHistory: []  
      });
    } else if (action === 'addonredo') {
      url = url.replace('http://localhost:4720/', '');
      this.setState({ 
        history: [...this.state.history, url],
      });
    } else if (action === 'undo') {
      this.setState({ 
        history: this.state.history.slice(0, this.state.history.length - 1),
        undoHistory: [...this.state.undoHistory, url],
        url: url
      });
    } else if (action === 'redo') {
      this.setState({ 
        history: [...this.state.history, url],
        undoHistory: this.state.undoHistory.slice(0, this.state.undoHistory.length - 1), 
      });
      this.setImageURLOnRedo(url);
    } else if (action === 'reset') {
      this.setState({ 
        history: [this.initImg],
        undoHistory: [],
        url: this.initImg,
      });
    }
  }


  render() {
    return (
      <div style={{ height: '100vh' }}>
        <ResizableColumns
          left={
            <>
              <DropdownList url={this.state.url} setImageURL={this.setImageURL} 
                original={this.state.originalURL} setOriginal={this.setOriginalURL}
                history={this.state.history} modifyHistory={this.modifyHistory}
                undoHistory={this.state.undoHistory}
              />
              <div style={{ margin: '8px' }}>
                <Dropdown title='Crop' content={<Crop url={this.state.url} setImageURL={this.setImageURL} />} icon={<BiCrop size={28} />} />
                <Dropdown title='Flip' content={<Flip url={this.state.url} setImageURL={this.setImageURL} />} icon={<MdFlip size={28} />} />
                <Dropdown title='Scale' content={<Scale url={this.state.url} setImageURL={this.setImageURL} />} icon={<MdOutlinePhotoSizeSelectLarge size={28} />} />
                <Dropdown title='Rotate' content={<Rotate url={this.state.url} setImageURL={this.setImageURL} />} icon={<MdOutlineRotate90DegreesCw size={28} />} />
                <Dropdown title='Linear Map' content={<LinearMap url={this.state.url} setImageURL={this.setImageURL} />} icon={<AiOutlineAreaChart size={28} />} />
                <Dropdown title='Power Law Map' content={<PowerLaw url={this.state.url} setImageURL={this.setImageURL} />} icon={<BsPower size={28} />} />
                <Dropdown title='Histogram' content={<Histogram url={this.state.url} />} icon={<GiHistogram size={28} />} />
                <Dropdown title='Histogram Equalization' content={<HistogramEqualization url={this.state.url} setImageURL={this.setImageURL} />} icon={<BiEqualizer size={28} />} />
                <Dropdown title='Convolution' content={<Convolution url={this.state.url} setImageURL={this.setImageURL} />} icon={<BsGrid3X3Gap size={28} />} />
                <Dropdown title='Salt and Pepper Noise' content={<SaltPepper url={this.state.url} setImageURL={this.setImageURL} />} icon={<TbSalt size={28} />} />
                <Dropdown title='Non-Linear Filter' content={<NonLinearFilter url={this.state.url} setImageURL={this.setImageURL} />} icon={<IoFilterSharp size={28} />} />
                <Dropdown title='Shear' content={<Shear url={this.state.url} setImageURL={this.setImageURL} />} icon={<TbPolygon size={28} />} />
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
