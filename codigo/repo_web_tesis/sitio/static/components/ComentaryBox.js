const { Grid, Box, TextareaAutosize, Button, Link } = MaterialUI;

class ComentaryBox extends ConnectedComponent {
    constructor(props) {
        super(props);

        this.id = _.uniqueId('comentary-box');

        this.onClick = this.onClick.bind(this);
        this.btnCancelClick = this.btnCancelClick.bind(this);
        this.btnReplyClick = this.btnReplyClick.bind(this);

        this.level = props.level || 0;
        this.user = props.user || null;
        this.comment = props.comment || null;

        if (this.dataSourceURL) {
            this.dataSourceURL += `?padre_id=${this.comment ? this.comment.id : ''}`;
        }

        this.state = {
            comentaries: [],
            boxOpen: this.comment == null
        };
    }

    parseComentary(comentary) {
        return {
            id: comentary.pk,
            padre_id: this.comment ? this.comment.padre_id || this.comment.id : null,
            responde_id: this.comment ? this.comment.id : null,
            texto: comentary.fields.texto || null,
            fecha_creacion: comentary.fields.fecha_creacion && new Date(comentary.fields.fecha_creacion),
            usuario: {},
            responde: comentary.fields.responde_a_comentario && {
                id: comentary.fields.responde_a_comentario.pk,
                autor: {
                    id: comentary.fields.responde_a_comentario.fields.autor.pk,
                    username: comentary.fields.responde_a_comentario.fields.autor.fields.username,
                    imagen_url: comentary.fields.responde_a_comentario.fields.autor.fields.imagen_url || null,
                    perfil_url: comentary.fields.responde_a_comentario.fields.autor.fields.perfil_url || null
                }
            },
            autor: {
                id: comentary.fields.autor.pk,
                username: comentary.fields.autor.fields.username,
                imagen_url: comentary.fields.autor.fields.imagen_url || null,
                perfil_url: comentary.fields.autor.fields.perfil_url || null
            }
        }
    }

    parseJsonResponse(data) {
        const comentaries = [];

        for (const comentary of data) {
            comentaries.push(this.parseComentary(comentary));
        }

        return { comentaries };
    }

    addComment() {
        const commentBox = document.querySelector('#' + this.id + ' .comment-input');

        if (commentBox) {
            const comment = {
                texto: commentBox.value,
                padre_id: this.comment ? this.comment.padre_id : null,
                responde_id: this.comment ? this.comment.id : null
            };

            if (comment.padre_id === null) {
                comment.padre_id = comment.responde_id;
            }

            commentBox.value = null;

            if (comment.texto) {
                this.sendJsonRequest(comment);
                this.focusNewData();
            }
        }
    }

    onClick() {
        this.addComment();

        if (this.comment) {
            this.closeBox();
        }
    }

    btnCancelClick() {
        this.closeBox();
    }

    btnReplyClick() {
        this.openBox();
    }

    openBox() {
        this.setState((prev) => ({
            boxOpen: true
        }))
    }

    closeBox() {
        this.setState((prev) => ({
            boxOpen: false
        }))
    }

    focusNewData() {
        const end = document.querySelector('#' + this.id + ` #comentaries-end-${this.comment ? this.comment.id : 'root'}`);

        if (!isInViewport(end)) {
            window.scroll(0, findElementPosY(end) - 200);
        }
    }

    fetchData(isInitialFetch = false) {
        if (this.level <= 1) {
            super.fetchData(isInitialFetch);
        }
    }

    render() {
        const comentaries = [];

        for (let idx = 0; idx < this.state.comentaries.length; idx++) {
            const comentary = this.state.comentaries[idx];

            const comentaryComponent = (
                <Box className="comentary" key={idx}>
                    <Grid container wrap="nowrap" justifyContent="flex-start" spacing={2}>
                        <Grid item>
                            <Avatar component={Link} href={comentary.autor.perfil_url} alt={comentary.autor.username} src={comentary.autor.imagen_url} />
                        </Grid>

                        <Grid item xs zeroMinWidth>

                            <p style={{ margin: 0, marginTop: '5px', textAlign: "left", color: "gray" }}>
                                <Link style={{ marginRight: '10px' }} href={comentary.autor.perfil_url}>{comentary.autor.username}</Link>
                                <span>{comentary.fecha_creacion && comentary.fecha_creacion.toLocaleString()}</span>
                            </p>

                            <p style={{ textAlign: "left", marginBottom: '5px' }}>
                                {(comentary.responde && comentary.responde.autor.id !== comentary.autor.id) && (
                                    <Link style={{ marginRight: '5px' }} href={comentary.responde.autor.perfil_url}>@{comentary.responde.autor.username}</Link>
                                )} <span>{comentary.texto}{" "}</span>
                            </p>

                        </Grid>
                    </Grid>

                    <Box style={{ paddingLeft: '40px', paddingBottom: 0, paddingTop: 0 }}>
                        <ComentaryBox {...this.props} level={this.level + 1} connectedParent={this} comment={comentary} />
                    </Box>
                </Box>
            );

            comentaries.push(comentaryComponent);
        }

        return (
            <Box id={this.id}>

                {(this.comment && this.user && (this.comment.autor.id !== this.user.pk)) && (<Button onClick={this.btnReplyClick} name="action" role="submit" type="submit" value="REPLY" style={{ marginTop: 0, marginLeft: '15px', padding: '2px', marginBottom: '15px' }}>Responder</Button>)}

                {
                    this.state.boxOpen &&
                    (<Grid container className="gridContainer" style={{ marginTop: '15px', marginBottom: '10px', padding: 0 }}>
                        <Grid xs={12} sm={9} item className="gridItem">
                            <TextareaAutosize
                                className="comment-input"
                                tabIndex="0"
                                style={{ width: '100%', maxHeight: '95px', minHeight: '40px', resize: 'none' }}
                                {...this.props.InputProps}
                                placeholder="Escribe un comentario..."
                            ></TextareaAutosize>
                        </Grid>

                        <Grid xs={12} item className="gridItem">
                            {this.user ? (<Button onClick={this.onClick} name="action" role="submit" type="submit" value="COMENTAR" variant="outlined" style={{ marginTop: '10px', marginLeft: '2px' }}>Comentar</Button>) : (<p>Para comentar primero debes ingresar con tu cuenta.</p>)}
                            {this.comment && (<Button onClick={this.btnCancelClick} name="action" role="submit" type="submit" value="CANCELAR" variant="outlined" style={{ marginTop: '10px', marginLeft: '15px' }}>Cancelar</Button>)}
                        </Grid>
                    </Grid>)
                }

                {comentaries}

                <div id={`comentaries-end-${this.comment ? this.comment.id : 'root'}`}></div>

            </Box>
        )
    }
}
