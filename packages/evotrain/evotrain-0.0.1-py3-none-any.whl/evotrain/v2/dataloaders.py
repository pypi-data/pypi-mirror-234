

def get_dataloaders(im_path,
                    classes,
                    bands,
                    mask_path=None,
                    batch_size=10,
                    augment=False,
                    split_perc=.15,
                    ):

    im_transforms = _transforms(augment)

    if mask_path:
        train_dataset, valid_dataset = _get_dataset_segmentation_dataset(im_path,
                                                                         classes,
                                                                         bands,
                                                                         mask_path,
                                                                         im_transforms,
                                                                         split_perc,
                                                                         )
    else:
        train_dataset, valid_dataset = _get_segmentation_dataset2(im_path,
                                                                  classes,
                                                                  bands,
                                                                  im_transforms,
                                                                  split_perc,
                                                                  )

    train_loader = DataLoader(
        train_dataset, batch_size=batch_size, shuffle=True, num_workers=12)
    valid_loader = DataLoader(
        valid_dataset, batch_size=1, shuffle=False, num_workers=4)
    return train_dataset, valid_dataset, train_loader, valid_loader
