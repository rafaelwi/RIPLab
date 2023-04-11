import '../css/ImageView.css';
import { ImageReaderProp } from '../common/types';


function ImageView(props: ImageReaderProp) {
  return (
    <div className="image-view">
      <img id="image-view-img" src={props.url} alt="uploaded" />
    </div>
  );
}

export default ImageView;
