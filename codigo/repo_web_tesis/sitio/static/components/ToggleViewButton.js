const { Button, Icon, Popper } = MaterialUI;

class ToggleViewButton extends React.Component {
    constructor(props) {
        super(props);
        
        this.onClick = this.onClick.bind(this);

        this.state = {
            anchorEl: null
        };
    }

    setAnchorEl(value) {
        this.setState(prev => ({ anchorEl: value }));
    }

    onClick(event) {
        this.setAnchorEl(this.state.anchorEl ? null : event.currentTarget);
    }

    render() {
        const { text, children, variant, style } = this.props;

        const open = Boolean(this.state.anchorEl);
        const id = open ? 'notifications-popper' : undefined;

        const button = (
            <div style={{ float: 'left', ...style }}>
                <Button type="button" aria-describedby={id} color="primary" variant={variant || 'contained'} onClick={this.onClick}>
                    { text || 'Toggle View' }
                </Button>

                <Popper 
                placement="bottom"
                id={id}
                open={open}
                anchorEl={this.state.anchorEl}
                style={{zIndex: 9999}}
                >
                    <Box sx={{ border: '1px solid black', p: 0, bgcolor: 'background.paper', zIndex: 9999 }}>
                        { children }
                    </Box>
                </Popper>
            </div>
        );

        return button;
    }
}