const sharp = require('sharp');
const path = require('path');
const fs = require('fs');

// This dirname corresponds to the absolute path of the project, being: /Path/To/S18GW_CNN
const DIRNAME = path.join(__dirname, '../..');
const FILES_FOLDER_NAME = 'Files';

// These constants refer to the "relative" paths of the folders where the unresized images are stored
// "relative" because they are relative to the root of S18GW_CNN.
const GW_RELATIVE_PATH = `${FILES_FOLDER_NAME}/qtransform`;
const NOISE_RELATIVE_PATH = `${FILES_FOLDER_NAME}/noise`;

// These constants refer to the "relative" paths of the folders where the resized images will be stored
// "relative" because they are relative to the root of S18GW_CNN.
const RD_GW_RELATIVE_PATH = `${FILES_FOLDER_NAME}/qtransform_rd`;
const RD_NOISE_RELATIVE_PATH = `${FILES_FOLDER_NAME}/noise_rd`;

// These constants refer to the absolute paths of where the unresized images are stored
const GW_ABSOLUTE_PATH = `${DIRNAME}/${GW_RELATIVE_PATH}`;
const NOISE_ABSOLUTE_PATH = `${DIRNAME}/${NOISE_RELATIVE_PATH}`;

// These constants refer to the absolute paths of where the resized images will be stored
const RD_GW_ABSOLUTE_PATH = `${DIRNAME}/${RD_GW_RELATIVE_PATH}`;
const RD_NOISE_ABSOLUTE_PATH = `${DIRNAME}/${RD_NOISE_RELATIVE_PATH}`;

async function generateFolder(path) {
  try {
    await fs.mkdirSync(path);
  } catch (e) {
    throw new Error(`Error happened while modifying path: ${path} (generatingFolder): ${e}`);
  }
}

async function checkAndCreateRdPaths() {
  const rdGwExists = fs.existsSync(RD_GW_ABSOLUTE_PATH);
  const rdNoiseExists = fs.existsSync(RD_NOISE_ABSOLUTE_PATH);

  if (rdGwExists) {
    const isDirectory = fs.lstatSync(RD_GW_ABSOLUTE_PATH).isDirectory();
    if (!isDirectory) throw new Error(`Path: ${RD_GW_ABSOLUTE_PATH} exists but its not a directory`);
  } else {
    await generateFolder(RD_GW_ABSOLUTE_PATH);
  }

  if (rdNoiseExists) {
    const isDirectory = fs.lstatSync(RD_NOISE_ABSOLUTE_PATH).isDirectory();
    if (!isDirectory) throw new Error(`Path: ${RD_NOISE_ABSOLUTE_PATH} exists but its not a directory`);
  } else {
    await generateFolder(RD_NOISE_ABSOLUTE_PATH);
  }
}

async function checkIfFolderContainsFiles(path) {
  return Boolean(await fs.readdirSync(path).length);
}

async function checkOriginalImagePaths() {
  const gwExists = fs.existsSync(GW_ABSOLUTE_PATH);
  const noiseExists = fs.existsSync(NOISE_ABSOLUTE_PATH);

  if (gwExists) {
    const isDirectory = fs.lstatSync(GW_ABSOLUTE_PATH).isDirectory();
    if (isDirectory) {
      const hasFiles = await checkIfFolderContainsFiles(GW_ABSOLUTE_PATH);
      if (!hasFiles) throw new Error(`Path: ${GW_ABSOLUTE_PATH} is empty. Did you ran all Python files first?`);
    } else {
      throw new Error(`Path: ${GW_ABSOLUTE_PATH} is not a directory. Did you ran all Python files first?`);
    }
  } else {
    throw new Error(`Path: ${GW_ABSOLUTE_PATH} does not exist. Did you ran all Python files first?`);
  }

  if (noiseExists) {
    const isDirectory = fs.lstatSync(NOISE_ABSOLUTE_PATH).isDirectory();
    if (isDirectory) {
      const hasFiles = await checkIfFolderContainsFiles(NOISE_ABSOLUTE_PATH);
      if (!hasFiles) throw new Error(`Path: ${NOISE_ABSOLUTE_PATH} is empty. Did you ran all Python files first?`);
    } else {
      throw new Error(`Path: ${NOISE_ABSOLUTE_PATH} is not a directory. Did you ran all Python files first?`);
    }
  } else {
    throw new Error(`Path: ${NOISE_ABSOLUTE_PATH} does not exist. Did you ran all Python files first?`);
  }
}

async function createRdFolders() {
  const gwDirs = fs.readdirSync(GW_ABSOLUTE_PATH);
  const noiseDirs = fs.readdirSync(NOISE_ABSOLUTE_PATH);
  for (const dir of gwDirs) {
    fs.mkdirSync(`${RD_GW_ABSOLUTE_PATH}/${dir}`);
  }
  for (const dir of noiseDirs) {
    fs.mkdirSync(`${RD_NOISE_ABSOLUTE_PATH}/${dir}`);
  }
}

async function redimensionFiles() {
  const gwDirs = fs.readdirSync(GW_ABSOLUTE_PATH);
  const noiseDirs = fs.readdirSync(NOISE_ABSOLUTE_PATH);
  for (const dir of gwDirs) {
    const imagePaths = fs.readdirSync(`${GW_ABSOLUTE_PATH}/${dir}`);
    for (const path of imagePaths) {
      await sharp(`${GW_ABSOLUTE_PATH}/${dir}/${path}`)
        .resize(32, 16, { kernel: sharp.kernel.nearest })
        .ignoreAspectRatio()
        .toFile(`${RD_GW_ABSOLUTE_PATH}/${dir}/RD_${path}`); 
    }
  }
  for (const dir of noiseDirs) {
    const imagePaths = fs.readdirSync(`${NOISE_ABSOLUTE_PATH}/${dir}`);
    for (const path of imagePaths) {
      await sharp(`${NOISE_ABSOLUTE_PATH}/${dir}/${path}`)
        .resize(32, 16, { kernel: sharp.kernel.nearest })
        .ignoreAspectRatio()
        .toFile(`${RD_NOISE_ABSOLUTE_PATH}/${dir}/RD_${path}`); 
    }
  }
}

(async () => {
  await checkAndCreateRdPaths();
  await checkOriginalImagePaths();
  await createRdFolders();
  await redimensionFiles();
})();