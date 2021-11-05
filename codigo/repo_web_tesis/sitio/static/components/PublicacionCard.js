const withStyles = MaterialUI.withStyles;

const Card = MaterialUI.Card;
const CardHeader = MaterialUI.CardHeader;
const CardMedia = MaterialUI.CardMedia;
const CardContent = MaterialUI.CardContent;
const CardActions = MaterialUI.CardActions;
const CardActionArea = MaterialUI.CardActionArea;
const Link = MaterialUI.Link;
const Collapse = MaterialUI.Collapse;
const Avatar = MaterialUI.Avatar;
const IconButton = MaterialUI.IconButton;
const Typography = MaterialUI.Typography;
const Icon = MaterialUI.Icon;

const red = MaterialUI.colors.red;
const grey = MaterialUI.colors.grey;

class PublicacionCard extends React.Component {
    static useStyles = (theme) => ({
        root: {

        },
        media: {
            height: 0,
            paddingTop: '56.25%', // 16:9
        },
        avatar: {
            backgroundColor: red[500],
            float: 'left',
            border: '2px solid white',
        },
        avatarPlus: {
            backgroundColor: grey[500],
            float: 'left',
            border: '2px solid white',
        }
    });

    constructor(props) {
        super(props);

        this.state = {
        }
    }

    render() {
        const { classes, usuario, titulo, fecha, resumen, resumenTitle, ver, imagen } = this.props;

        const usuarios = usuario ? [usuario] : [];
        const usuariosAvatar = [];

        let key = 0;

        for (const user of usuarios) {
            const display = user.fields.username.toLowerCase();
            const imagen = user.fields.imagen_url || null;

            const style = { zIndex: (usuarios.length - key) + 1 };

            if (key > 0) {
                style.marginLeft = '-12px';
            }

            usuariosAvatar.push(
                <Avatar component={Link} key={key} href={usuario.fields.perfil_url} src={imagen} style={style} aria-label={'@' + display} alt={'@' + display} className={classes.avatar}>
                    {!imagen ? `${display}` : null}
                </Avatar>
            )

            key++;
        }

        let parsedAvatars = [];

        if (usuariosAvatar.length > 2) {
            parsedAvatars.push(usuariosAvatar[0]);
            parsedAvatars.push(usuariosAvatar[1]);

            parsedAvatars.push(
                <Avatar style={{ zIndex: 1, marginLeft: '-12px' }} key={key + 1} aria-label='hay mas usuarios' alt='hay mas usuarios' className={classes.avatarPlus}>
                    {`+${usuariosAvatar.length - 2}`}
                </Avatar>
            );
        }
        else {
            parsedAvatars = usuariosAvatar;
        }

        return (
            <Card className={classes.root}>
                {
                    usuarios || titulo ?
                        <CardHeader
                            avatar={
                                <div>
                                    {parsedAvatars}
                                </div>
                            }
                            action={
                                usuarios ?
                                    <IconButton aria-label="settings">
                                        <Icon>more_vert</Icon>
                                    </IconButton> : null
                            }
                            {...(titulo ? { title: titulo } : {})}
                            subheader={
                                usuario ? (<span>
                                    <span>by <Link href={usuario && usuario.fields.perfil_url || ''}>{usuario && '@' + usuario.fields.username || ''}</Link></span> on <span>{fecha}</span>
                                </span>) : (<span>on {fecha}</span>)
                            }
                        /> : null
                }
                <CardActionArea component={Link} href={ver}>
                    {
                        imagen ?
                            (<CardMedia
                                className={classes.media}
                                image={imagen}
                                title={titulo}
                            />) : null
                    }
                    <CardContent>
                        <Typography variant="body1" color="textSecondary" component="p">
                            {resumenTitle}
                        </Typography>
                        <Typography variant="body1" color="textSecondary" component="p">
                            {resumen}
                        </Typography>
                    </CardContent>
                </CardActionArea>
                {
                    usuarios.length ?
                        (<CardActions disableSpacing>
                            <IconButton aria-label="like">
                                <Icon className="material-icons-outlined">thumb_up</Icon>
                            </IconButton>
                            <IconButton aria-label="share">
                                <Icon>share</Icon>
                            </IconButton>
                        </CardActions>) : null
                }
            </Card>
        );
    }
}

PublicacionCard = withStyles(PublicacionCard.useStyles)(PublicacionCard);
