
const scrollTriggerStyles = MaterialUI.makeStyles((theme) => ({
    root: {
        position: 'fixed',
        bottom: theme.spacing(6),
        right: theme.spacing(65),
        [theme.breakpoints.down('sm')]: {
            right: theme.spacing(3),
            bottom: theme.spacing(5),
        }
    },
}));

function ScrollTrigger(props) {
    const { children } = props;
    const classes = scrollTriggerStyles();
    const trigger = MaterialUI.useScrollTrigger({
        disableHysteresis: true,
        threshold: 100,
    });

    const handleClick = (event) => {
        const anchor = (event.target.ownerDocument || document).querySelector(props.anchor);

        if (anchor) {
            anchor.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }
    };

    return (
        <MaterialUI.Zoom in={trigger}>
            <div onClick={handleClick} role="presentation" className={classes.root}>
                {children}
            </div>
        </MaterialUI.Zoom>
    )
};

class GoUpButton extends React.Component {
    constructor(props) {
        super(props);
    }

    render() {
        return (
            <ScrollTrigger anchor={this.props.anchor}>
                <MaterialUI.Fab {...this.props} className="btn-subir" color="secondary" size="medium" aria-label="scroll back to top">
                    <MaterialUI.Icon>expand_less</MaterialUI.Icon>
                </MaterialUI.Fab>
            </ScrollTrigger>
        )
    }
}
