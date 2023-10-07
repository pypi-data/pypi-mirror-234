def train_wrapper(*,
                  logs_folder,
                  model_name,
                  im_path,
                  bands,
                  classes,
                  mask_path=None,
                  architecture="Unet",
                  backbone="mobilenet_v2",
                  activation="softmax2d",
                  loss="dice",
                  data_augmentation=True,
                  max_epochs=3,
                  learning_rate=1e-3,
                  batch_size=10,
                  resume=True,
                  gpus=1):

    model_kwargs = dict(in_channels=len(bands),
                        classes=classes,
                        arch=architecture,
                        backbone=backbone,
                        activation=activation,
                        loss=loss,
                        learning_rate=learning_rate,
                        bands=bands,
                        )
    logger.info("Getting dataloaders")
    _, valid_dataset, train_loader, valid_loader = get_dataloaders(im_path,
                                                                   classes,
                                                                   bands,
                                                                   mask_path,
                                                                   batch_size,
                                                                   im_transforms=data_augmentation,
                                                                   split_perc=.15,
                                                                   )

    logger.info("STARTING TRAINING")
    model = train_evolandnet(
        Path(logs_folder),
        model_name,
        train_loader,
        valid_loader,
        valid_dataset,
        model_kwargs,
        max_epochs=max_epochs,
        resume=resume,
        gpus=gpus)

    logger.info("TRAINING DONE")
    return model
