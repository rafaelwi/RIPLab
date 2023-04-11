import '../css/ImageOperations.css';
import {TbFlipHorizontal, TbFlipVertical} from 'react-icons/tb';
import { ImageOperationProp } from '../common/types';
import { sendCommonRequest } from '../common/utils';


function Flip(props: ImageOperationProp) {
  const horizontalFlip = async () => {
    // Make request
      sendCommonRequest(
        'http://localhost:4720/horizontal-flip',
        JSON.stringify({ url: props.url }),
        props.setImageURL
      );
    }

    const verticalFlip = async () => {
      // Make request
        sendCommonRequest(
          'http://localhost:4720/vertical-flip',
          JSON.stringify({ url: props.url }),
          props.setImageURL
        );
      }


  return (
    <div className="img-operation">
      <div className="operation-btn" onClick={horizontalFlip}>
        <div className="operation-icon"><TbFlipHorizontal size={20}/></div>
        <h3>Horizontal</h3>
      </div>
      <div className="operation-btn" onClick={verticalFlip}>
        <div className="operation-icon"><TbFlipVertical size={20}/></div>
        <h3>Vertical</h3>
      </div>
    </div>
  );
}

export default Flip;
