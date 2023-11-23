import Button from 'react-bootstrap/Button';
import ButtonGroup from 'react-bootstrap/ButtonGroup';
import ButtonToolbar from 'react-bootstrap/ButtonToolbar';

const FeatureButtons = () => {
    return (
        <ButtonToolbar className="justify-content-center" aria-label="Toolbar with feature buttons">
            <ButtonGroup className="me-2" aria-label="Service Management">
                <Button href="/service">Service Management</Button>
            </ButtonGroup>
            <ButtonGroup className="me-2" aria-label="PKG Population">
                <Button href="/population">Populate PKG</Button>
            </ButtonGroup>
            <ButtonGroup aria-label="PKG Exploration">
                <Button href="/explore">Explore PKG</Button>
            </ButtonGroup>
        </ButtonToolbar>
    );
}

export default FeatureButtons;