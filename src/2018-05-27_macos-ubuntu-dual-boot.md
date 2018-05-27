Title: Installing Ubuntu alongside macOS
Tags: macos, linux, ubuntu, system administration
Status: draft
Summary: Documentation of my experience installing Ubuntu on Apple hardware while keeping macOS intact.

This a guide on how to install Ubuntu with encrypted disk alongside macOS. The end result is that both operating
systems are bootable using the default Apple boot loader.

## 6 whys

*Why Linux?*
*Why Ubuntu?*
*Why LVM?*
*Why keep macOS?*
*Why not rEFIt?*
*Why not GRUB?*

Pre-requisites:

1. A device with macOS
2. Two USB flash drives: one for the macOS recovery and another for the Ubuntu installer

## Create macOS recovery USB stick

Follow https://support.apple.com/en-us/HT201372

```shell
sudo /Applications/Install\ macOS\ High\ Sierra.app/Contents/Resources/createinstallmedia \
    --volume /Volumes/MyVolume \
    --applicationpath /Applications/Install\ macOS\ High\ Sierra.app
```

## Create a bootable Ubuntu USB stick

Follow https://tutorials.ubuntu.com/tutorial/tutorial-create-a-usb-stick-on-macos#0

TL;DR:

1. Download Ubuntu ISO.
1. Use *Disk Utility* to reformat the USB stick into *MS-DOS (FAT)* format with *GUID Partition Map* scheme.
1. Convert Ubunto ISO to a format that can be written to the USB stick directly:

        :::shell
        hdiutil convert \
            -format UDRW \
            -o ~/Downloads/ubuntu-18.04-desktop-amd64.img \
            ~/Downloads/ubuntu-18.04-desktop-amd64.iso

1. Look up USB stick device name in `diskutil list` output.
1. Unmount the USB stick with `diskutil unmountDisk /dev/diskN` where `N` is from the previous step.
1. Write the content of the Ubuntu image to the USB stick:

        :::shell
        sudo dd \
            if=~/Downloads/ubuntu-18.04-desktop-amd64.img \
            of=/dev/rdiskN \
            bs=1m

   If macOS complains that the USB disk is unreadable, ignore the popup.
1. Run `diskutil eject /dev/diskN`

## Make disk space for the Ubuntu installation

In *Disk Utility* do the following:

1. Check *Show All Devices* from the *View* menu.
1. Select the disk where you want Ubuntu installed (make sure to select the disk and not a container or partition).
1. Select *Partition*. Confirm that partitioning is required if Disk Utility asks about adding and APFS volume instead.
1. Create two partitions:
   1. *Mac OS Extended (Journaled)* partition of size 512M, called *Ubuntu Boot*.
   1. *MS-DOS (FAT)* partition of arbitrary size. The size will be allocated into root, home and swap partitions
      later during the installation process. The name doesn't matter at this stage.

From the terminal, run

```shell
sudo bless --device /dev/diskNsM
```

where `diskNsM` is the *Ubuntu Boot* partition from the `diskutil list` output.

## Ubuntu installation

### Boot into the installer

Plug in the bootable Ubuntu USB stick and restart the computer. Hold the *Option* key during the boot in order
to have the boot menu opened. Select *EFI Boot*, then in the Ubuntu boot screen select *Try Ubuntu*.

### Partition the disk

1. Launch *Terminal*.
1. Start cgdisk with `sudo cgdisk /dev/sda`
1. Drop the last partition (MS-DOS partition created from macOS).
1. Create an LVM partition (type 8e00) on its place.

**Achtung**: `sda5` in the guide below is assuming macOS had three partitions and you've created one for Ubuntu Boot:

* sda1: macOS EFI boot partition
* sda2: macOS partition
* sda3: macOS recovery partition
* sda4: Ubuntu boot partition
* sda5: Ubuntu LVM partition

### Enable disk encryption

We will use so-called LVM on LUKS approach where a single LVM partition is LUKS-encrypted together with its volumes.

1. Initialise an encrypted parition: `cryptsetup luksFormat /dev/sda5`
1. Open the encrypted partition and map it as *lvm* `cryptsetup luksOpen /dev/sda5 lvm`

As the result, the partition is mapped as `/dev/mapper/lvm`.

### Create LVM volumes and file systems

```shell
# Initialise the disk to use LVM
pvcreate /dev/mapper/lvm
# Create an LVM volume group called "my-encrypted"
vgcreate my-encrypted /dev/mapper/lvm
# Create an LVM volume for swap, size of the computer RAM
lvcreate -L 4G my-encrypted -n swap
# Create an LVM volume for the root filesystem
lvcreate -L 20G my-encrypted -n root
# Create an LVM volume for /home
lvcreate -l +100%FREE my-encrypted -n home
# Create file systems
mkfs.ext4 /dev/mapper/my-encrypted-root
mkfs.ext4 -m 1 /dev/mapper/my-encrypted-home
mkswap /dev/mapper/my-encrypted-swap
# Label the volumes
e2label /dev/mapper/my-encrypted-root "Root"
e2label /dev/mapper/my-encrypted-home "Home"
```

### Install Ubuntu

Launch the installer by calling `ubiquity --no-bootloader` - note the command-line argument.

Proceed until the disk partitioning step, choose "Something else" there and use the following mapping,
keep *format* unchecked:

* map `/dev/mapper/my-root-volume` to `/`.
* map `/dev/mapper/my-home-volume` to `/home`.
* map `/dev/sda4` to `/boot`.

### Chroot

```shell
mount /dev/mapper/my-root-volume /mnt
cd /mnt
mount -t proc /proc proc/
mount --rbind /sys sys/
mount --rbind /dev dev/
mount --rbind /run run/
mkdir /mnt/boot
mount /dev/sda4 /mnt/boot
```

Then `chroot /mnt /bin/bash`

### Check /etc/fstab

Make sure everything is in order.

### Setup GRUB

In the chroot environment, install GRUB with `apt-get install grub-efi-amd64`

Then install the GRUB UEFI application into `/boot/EFI/arch/System/Library/CoreServices/boot.efi` and its modules into
`/boot/grub/x86_64-efi`

```shell
grub-install --target=x86_64-efi --efi-directory=/boot
```

Note: `touch /boot/efi/EFI/ubuntu/mach_kernel` if the last command doesn't work.

Create a GRUB configuration file

```shell
grub-mkconfig -o /boot/grub/grub.cfg
```

#### Add Ubuntu to the macOS boot loader

Change the directory structure to match macOS expectations:

```shell
mv /boot/efi/EFI/arch/System/ /boot/
rm -r /boot/EFI/
```

Create a dummy `mach_kernel` file:

```shell
echo "This file is required for booting" > /boot/mach_kernel
```

Create a file `/boot/System/Library/CoreServices/SystemVersion.plist` with the following content:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<plist version="1.0">
<dict>
    <key>ProductBuildVersion</key>
    <string></string>
    <key>ProductName</key>
    <string>Linux</string>
    <key>ProductVersion</key>
    <string>Ubuntu</string>
</dict>
</plist>
```

TODO: May need to bless the boot.efi file again?

#### Adding an Ubuntu icon to the Apple boot loader

1. Install `wget`, `librsvg` and `libicns`.
1. Download Ubuntu clipart

        :::shell
        wget -O /tmp/ubuntu-clipart.zip https://assets.ubuntu.com/v1/9fbc8a44-circle-of-friends-web.zip
        unzip /tmp/ubuntu-clipart.zip

1. Resize the logo to 128x128 pixels and convert it to icns format

        :::shell
        rsvg-convert -w 128 -h 128 -o /tmp/ubuntu-logo.png XXX_
        png2icns /tmp/ubuntu-logo.icns /tmp/ubuntu-logo.png

1. Put the logo in the location where macOS boot loader can find it

        :::shell
        sudo cp /tmp/ubuntu-logo.icns /boot/.VolumeIcon.icns

1. Cleanup

        :::shell
        rm /tmp/ubuntu-logo.icns
        rm /tmp/ubuntu-logo.png
        rm /tmp/ubuntu-clipart.zip
   
