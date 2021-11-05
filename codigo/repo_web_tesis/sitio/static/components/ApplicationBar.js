const withStyles = MaterialUI.withStyles;

const AppBar = MaterialUI.AppBar;
const Toolbar = MaterialUI.Toolbar;
const Typography = MaterialUI.Typography;
const Button = MaterialUI.Button;
const IconButton = MaterialUI.IconButton;
const Icon = MaterialUI.Icon;

class ApplicationBar extends React.Component {
    static styles = (theme) => ({
        root: {
            flexGrow: 1,
        },
        loginButton: {
            marginRight: theme.spacing(3)
        },
        menuButton: {
            marginRight: theme.spacing(2),
            [theme.breakpoints.up('md')]: {
                display: 'none'
            }
        },
        title: {
            flexGrow: 1,
        }
    });

    constructor(props) {
        super(props);
    }

    render() {
        const { classes, user, title, loginLink, profileLink, notifications } = this.props;

        const loginButton = user
            ? (<NotificationsButton {...(notifications || {})}></NotificationsButton>)
            : (
                <Button className={classes.loginButton} color="inherit" href={loginLink}>
                    <Icon style={{ marginRight: '6px' }}>login</Icon>
                    Ingresar
                </Button>
            );

        return (
            <AppBar position="fixed">
                <Toolbar>
                    <Typography variant="h6" className={classes.title}>
                        {title}
                    </Typography>

                    <div style={{ marginRight: '35%' }}>
                        {loginButton}
                    </div>

                    <IconButton edge="start" className={classes.menuButton} color="inherit" aria-label="menu">
                        <Icon>menu</Icon>
                    </IconButton>
                </Toolbar>
            </AppBar>
        )
    }
}

ApplicationBar = withStyles(ApplicationBar.styles)(ApplicationBar);
