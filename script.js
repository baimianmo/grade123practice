// 英文单词清单
const wordList = {
  "一年级上册": {
    "Unit 1": ["book", "ruler", "pencil", "schoolbag", "teacher", "I", "have", "a/an"],
    "Unit 2": ["face", "ear", "eye", "nose", "mouth", "this", "my", "is"],
    "Unit 3": ["dog", "bird", "cat", "tiger", "monkey", "it", "what"],
    "Unit 4": ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "how", "many", "there", "are"],
    "Unit 5": ["black", "red", "yellow", "green", "blue", "colour"],
    "Unit 6": ["apple", "pear", "banana", "orange", "you", "like", "yes", "no", "do"]
  },
  "一年级下册": {
    "Unit 1": ["chair", "desk", "blackboard", "under", "in", "where", "on"],
    "Unit 2": ["light", "box", "bed", "door", "near", "behind"],
    "Unit 3": ["plane", "ball", "doll", "train", "car", "bear", "can", "sure", "sorry"],
    "Unit 4": ["rice", "noodles", "vegetable", "fish", "chicken", "egg", "hungry", "want", "and"],
    "Unit 5": ["juice", "water", "tea", "milk", "thirsty", "thanks"],
    "Unit 6": ["shirt", "socks", "T-shirt", "shorts", "skirt", "dress", "your"]
  },
  "二年级上册": {
    "Unit 1": ["father", "mother", "brother", "sister", "grandmother", "grandfather", "who", "he", "she"],
    "Unit 2": ["classmate", "friend", "woman", "girl", "man", "boy", "look", "his", "her", "name", "or"],
    "Unit 3": ["big", "tall", "short", "thin", "handsome", "pretty", "new", "does"],
    "Unit 4": ["bookshop", "park", "zoo", "hospital", "school", "supermarket", "go", "to"],
    "Unit 5": ["grass", "tree", "flower", "boat", "lake", "hill"],
    "Unit 6": ["Christmas", "Father Christmas", "Christmas tree", "card", "present", "happy", "New Year", "thank", "merry", "here", "too"]
  }
};

// 游戏变量
let score = 0;
let timeLeft = 60;
let gameInterval;
let timerInterval;
let isGameRunning = false;
let difficulty = 3; // 3x3网格
let activeMoles = 0;
let maxActiveMoles = 2; // 初始最大同时出现的地鼠数量
let spawnRate = 1500; // 初始出现间隔(毫秒)

// DOM元素
const gameBoard = document.getElementById('gameBoard');
const startBtn = document.getElementById('startBtn');
const restartBtn = document.getElementById('restartBtn');
const timer = document.getElementById('timer');
const scoreDisplay = document.getElementById('score');
const gameOver = document.getElementById('gameOver');
const finalScore = document.getElementById('finalScore');
const hitSound = document.getElementById('hitSound');
const goldSound = document.getElementById('goldSound');
const missSound = document.getElementById('missSound');

// 初始化游戏板
function initGameBoard(size) {
  gameBoard.innerHTML = '';
  gameBoard.className = `grid gap-4 mb-6 grid-cols-${size}`;
  
  for (let i = 0; i < size * size; i++) {
    const hole = document.createElement('div');
    hole.className = 'hole';
    hole.dataset.index = i;
    gameBoard.appendChild(hole);
  }
}

// 获取随机单词
function getRandomWord() {
  const grades = Object.keys(wordList);
  const randomGrade = grades[Math.floor(Math.random() * grades.length)];
  const units = Object.keys(wordList[randomGrade]);
  const randomUnit = units[Math.floor(Math.random() * units.length)];
  const words = wordList[randomGrade][randomUnit];
  return words[Math.floor(Math.random() * words.length)];
}

// 创建地鼠
function createMole() {
  if (!isGameRunning || activeMoles >= maxActiveMoles) return;

  const holes = document.querySelectorAll('.hole');
  const emptyHoles = Array.from(holes).filter(hole => !hole.querySelector('.mole'));
  
  if (emptyHoles.length === 0) return;

  const randomHole = emptyHoles[Math.floor(Math.random() * emptyHoles.length)];
  const isGold = Math.random() < 0.1; // 10%概率金色地鼠
  
  const mole = document.createElement('div');
  mole.className = `mole ${isGold ? 'gold' : ''}`;
  
  const word = document.createElement('div');
  word.className = 'mole-word';
  word.textContent = getRandomWord();
  mole.appendChild(word);
  
  randomHole.appendChild(mole);
  activeMoles++;
  
  // 地鼠自动消失
  const duration = isGold ? 800 + Math.random() * 400 : 1000 + Math.random() * 1000;
  setTimeout(() => {
    if (mole.parentNode) {
      mole.remove();
      activeMoles--;
    }
  }, duration);
}

// 开始游戏
function startGame() {
  if (isGameRunning) return;
  
  isGameRunning = true;
  score = 0;
  timeLeft = 60;
  activeMoles = 0;
  maxActiveMoles = 2;
  spawnRate = 1500;
  
  scoreDisplay.textContent = score;
  timer.textContent = timeLeft;
  gameOver.classList.add('hidden');
  
  initGameBoard(difficulty);
  
  // 游戏主循环
  gameInterval = setInterval(() => {
    createMole();
    
    // 随时间增加难度
    if (timeLeft < 40 && maxActiveMoles < 3) maxActiveMoles = 3;
    if (timeLeft < 20 && maxActiveMoles < 4) maxActiveMoles = 4;
    if (timeLeft < 10) spawnRate = 800;
  }, spawnRate);
  
  // 倒计时
  timerInterval = setInterval(() => {
    timeLeft--;
    timer.textContent = timeLeft;
    
    if (timeLeft <= 0) {
      endGame();
    }
  }, 1000);
}

// 结束游戏
function endGame() {
  isGameRunning = false;
  clearInterval(gameInterval);
  clearInterval(timerInterval);
  
  // 移除所有地鼠
  document.querySelectorAll('.mole').forEach(mole => mole.remove());
  activeMoles = 0;
  
  finalScore.textContent = score;
  gameOver.classList.remove('hidden');
}

// 点击事件处理
gameBoard.addEventListener('click', (e) => {
  if (!isGameRunning) return;
  
  const mole = e.target.closest('.mole');
  const hole = e.target.closest('.hole');
  
  if (mole) {
    // 点击地鼠
    mole.classList.add('scale');
    
    const isGold = mole.classList.contains('gold');
    const points = isGold ? 30 : 10;
    
    score += points;
    scoreDisplay.textContent = score;
    
    if (isGold) {
      goldSound.currentTime = 0;
      goldSound.play();
    } else {
      hitSound.currentTime = 0;
      hitSound.play();
    }
    
    setTimeout(() => {
      mole.remove();
      activeMoles--;
    }, 100);
  } else if (hole && !hole.querySelector('.mole')) {
    // 点击空白区域
    score = Math.max(0, score - 5);
    scoreDisplay.textContent = score;
    missSound.currentTime = 0;
    missSound.play();
  }
});

// 按钮事件
startBtn.addEventListener('click', startGame);
restartBtn.addEventListener('click', startGame);

// 初始化3x3网格
initGameBoard(3);