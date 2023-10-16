import {
  IQuestion,
  parseCodeCell,
  parseStepsFromCells,
} from '@boyuai/jupyter-helper';
import { parseQuestionOptions } from '@boyuai/jupyter-helper/lib/quiz';
import { getQuizQuestionByUUID, parseQuizQuestions } from './services';
import { ICell, IJupyter } from './types';
import '../css/extension.css';

const Jupyter: IJupyter = (window as any)['Jupyter'];
export const workRegx = /work\/lessons-(\d+)-(\w+)\.ipynb/;

class BBYError extends Error {
  constructor(message: string, cellIndex?: number, detail?: string) {
    super(message);
    //@ts-ignore
    if (cellIndex) this.cellIndex = cellIndex;
    //@ts-ignore
    if (detail) this.detail = detail;
  }
}

export const registerBbyButtons = () => {
  Jupyter.toolbar.add_buttons_group([
    Jupyter.keyboard_manager.actions.register(
      {
        help: '同步课程',
        icon: 'fa-retweet',
        handler: syncLesson,
      },
      'sync-lesson',
      'ipybbycell'
    ),
  ]);
  Jupyter.toolbar.add_buttons_group([
    Jupyter.keyboard_manager.actions.register(
      {
        help: '添加「课程」',
        icon: 'fa-book',
        handler: addLesson,
      },
      'add-lesson',
      'ipybbycell'
    ),
  ]);
  Jupyter.toolbar.add_buttons_group([
    Jupyter.keyboard_manager.actions.register(
      {
        help: '添加「普通 Step」',
        icon: 'fa-font',
        handler: addStringStep,
      },
      'add-string-step',
      'ipybbycell'
    ),
    Jupyter.keyboard_manager.actions.register(
      {
        help: '添加「Verify Step」',
        icon: 'fa-columns',
        handler: addVerifyStep,
      },
      'add-verify-step',
      'ipybbycell'
    ),
    Jupyter.keyboard_manager.actions.register(
      {
        help: '添加「OJ Step」',
        icon: 'fa-magic',
        handler: addOjStep,
      },
      'add-oj-step',
      'ipybbycell'
    ),
    Jupyter.keyboard_manager.actions.register(
      {
        help: '添加「Matplotlib Step」',
        icon: 'fa-area-chart',
        handler: addMatplotlibStep,
      },
      'add-matplotlib-step',
      'ipybbycell'
    ),
    Jupyter.keyboard_manager.actions.register(
      {
        help: '添加「Turtle Step」',
        icon: 'fa-pencil',
        handler: addTurtleStep,
      },
      'add-turtle-step',
      'ipybbycell'
    ),
    Jupyter.keyboard_manager.actions.register(
      {
        help: '添加「Quiz Step」',
        icon: 'fa-question-circle',
        handler: addQuizStep,
      },
      'add-quiz-step',
      'ipybbycell'
    ),
    Jupyter.keyboard_manager.actions.register(
      {
        help: '添加「Upload File Step」',
        icon: 'fa-upload',
        handler: addUploadFileStep,
      },
      'add-upload-file-step',
      'ipybbycell'
    ),
    Jupyter.keyboard_manager.actions.register(
      {
        help: '添加「题解」',
        icon: 'fa-fire',
        handler: addSummary,
      },
      'add-summary',
      'ipybbycell'
    ),
    Jupyter.keyboard_manager.actions.register(
      {
        help: '添加「折叠块」',
        icon: 'fa-eye',
        handler: addDetailStep,
      },
      'add-detail-step',
      'ipybbycell'
    ),
    Jupyter.keyboard_manager.actions.register(
      {
        help: '添加「图片播放器」',
        icon: 'fa-image',
        handler: addImagePlayerStep,
      },
      'add-image-player-step',
      'ipybbycell'
    ),
    Jupyter.keyboard_manager.actions.register(
      {
        help: '添加「视频」',
        icon: 'fa-file-video-o',
        handler: addVideoPlayerStep,
      },
      'add-video-player-step',
      'ipybbycell'
    ),
    Jupyter.keyboard_manager.actions.register(
      {
        help: '添加「音频」',
        icon: 'fa-file-audio-o',
        handler: addAudioStep,
      },
      'add-audio-player-step',
      'ipybbycell'
    ),
    Jupyter.keyboard_manager.actions.register(
      {
        help: '添加「不可复制代码块」',
        icon: 'fa-code',
        handler: addUserSelectNoneCode,
      },
      'add-user-select-none-code',
      'ipybbycell'
    ),
  ]);

  Jupyter.toolbar.add_buttons_group([
    Jupyter.keyboard_manager.actions.register(
      {
        help: '添加「文件 Cell」',
        icon: 'fa-file',
        handler: addFileCell,
      },
      'add-file-cell',
      'ipybbycell'
    ),
  ]);
};

const insertCodeCellBelow = function (code: string) {
  Jupyter.notebook.insert_cell_below('code').set_text(code);
  Jupyter.notebook.select(Jupyter.notebook.get_selected_index()! + 1);
  Jupyter.notebook.focus_cell();
};

const insertMarkdownCellBelow = function (md: string) {
  Jupyter.notebook.insert_cell_below('markdown').set_text(md);
  Jupyter.notebook.select(Jupyter.notebook.get_selected_index()! + 1);
  Jupyter.notebook.focus_cell();
};

const insertCodeInCurrentMarkdownCell = function (md: string) {
  const currentIdx = Jupyter.notebook.get_selected_index();
  if (!currentIdx) {
    alert('请选中一个 Markdown Cell');
    return;
  };
  const current = Jupyter.notebook.get_cell(currentIdx!);
  if (current.cell_type !== 'markdown') {
    alert('请选中一个 Markdown Cell');
    return;
  }
  current.set_text(current.get_text() + '\n' + md);
}

const addStepDescCells = function () {
  insertMarkdownCellBelow('### 步骤标题');

  insertCodeCellBelow(`#platform-desc
from ipyaliplayer import Player
Player(vid='--替换你的视频id，上传地址 https://www.boyuai.com/elites/admin/public-video', aspect_ratio=4/3)
`);

  insertMarkdownCellBelow(`<!--步骤描述 -->

#### 知识点
- 总结视频中的知识点

#### 代码练习说明
- 代码练习题目说明

#### 代码练习提示
- 代码练习提示`);
};

const addStringStep = function () {
  addStepDescCells();

  insertCodeCellBelow(`#platform-lock-hidden

# platform-lock-hidden 的代码不会展示，但会被运行

def add(x):
  return x + 1`);

  insertCodeCellBelow(`#platform-edit

# platform-edit 可被学员编辑

$$$`);

  insertCodeCellBelow(`#platform-edit-answer

# 练习答案代码
# 我们提供“一键填入”功能将答案复制到对应的代码块中
# 建议 platform-edit-answer 块是直接在 platform-edit 块的基础上修改，并添加额外的解释说明

x = add(0)`);
  insertCodeCellBelow(`#platform-lock

# platform-lock 的代码会被展示和运行，无法修改
print("add(0) =", x)`);

  insertMarkdownCellBelow('add(0) = 1');
};

const addOjStep = function () {
  insertMarkdownCellBelow('### 步骤标题');

  insertCodeCellBelow(`#platform-desc
`);

  insertMarkdownCellBelow(`#### 题目描述

在此处填写题目描述

#### 输入描述

在此处填写输入描述

#### 输出描述

在此处填写输出描述

#### 输入样例

在此处填写输入样例

#### 输出样例

在此处填写输出样例
`);

  insertCodeCellBelow(`//platform-edit
#include <iostream>
using namespace std;

int main(){
    
    return 0;
}`);

  insertCodeCellBelow(`//platform-edit-answer
//参考答案
#include <iostream>
using namespace std;

int main(){

    
    return 0;
}`);

  insertMarkdownCellBelow(`ONLINE_JUDGE_PROBLEM_ID=XXX`);
}

const addLesson = function () {
  Jupyter.notebook.insert_cell_below('markdown').set_text(`## 单元标题

单元简介（目前不展示这部分，所以可以写的简单一点）`);
  Jupyter.notebook.delete_cells();

  addStringStep();
};

const addVerifyStep = function () {
  addStepDescCells();

  insertCodeCellBelow(`#platform-edit

def add(x):
  return x`);

  insertCodeCellBelow(`#platform-edit-answer

def add(x):
  return x + 1`);

  insertCodeCellBelow(`#platform-lock
print(add(1))`);
  insertCodeCellBelow(`#platform-verify
import json
if add(2) == 3 and add(-1) == 0:
  print(json.dumps({"result": True, "displayResult": "good"}))
else:
  print(json.dumps({"result": False, "displayResult": "bad"}))`);
};

const addMatplotlibStep = function () {
  addStepDescCells();

  insertCodeCellBelow(`#platform-edit

import matplotlib.pyplot as plt
plt.plot([1, 2, 3])
plt.show()`);

  insertCodeCellBelow(`#platform-edit-answer

import matplotlib.pyplot as plt
plt.plot([1, 2, 3, 4])
plt.show()`);

  insertCodeCellBelow(`#platform-lock-hidden

# 不要修改
print("#matplotlib#")`);

  insertMarkdownCellBelow('#matplotlib#');
};

const addTurtleStep = function () {
  addStepDescCells();

  insertCodeCellBelow(`#platform-lock
from ipyturtle2 import TurtleWidget

t = TurtleWidget()
t`);

  insertCodeCellBelow(`#platform-edit

t.forward(100)
t.left(90)
t.pencolor('red')
t.forward(100)
t.left(90)
t.forward(100)
t.left(90)
t.forward(100)`);

  insertCodeCellBelow(`#platform-edit-answer

t.forward(100)
t.left(90)
t.pencolor('blue')
t.forward(100)`);

  insertCodeCellBelow(`#platform-lock-hidden

# 不要修改
print("#turtle#")`);

  insertMarkdownCellBelow('#turtle#');
};

const quizString = `#platform-quiz
import ipyquiz
type = "normal"
quizzes = []

quizzes.append({
  "id": "fill-1",
  "type": "FILL",
  "title": "学习是系统通过____提升性能的过程。",
  "answer": "经验"
})

quizzes.append({
  "id": "fill-2",
  "type": "FILL",
  "title": """
试试**markdown**吧
$x+1$
""",
  "answer": "1"
})

quizzes.append({
  "id": "fill-3",
  "type": "FILL",
  "title": "填啥都行",
  "answer": ""
})

quizzes.append({
  "id": "choice-1",
  "type": "SELECT",
  "title": "matplotlib 绘制图形的基本组成包含文字部分和图形部分，以下说法错误的是：",
  "answer": "1",
  "options": [
      {
          "value": "0",
          "text": "图形标题、图例是基本组成中的文字部分。"
      },
      {
          "value": "1",
          "text": "x、y 坐标轴、刻度标签是基本组成中的文字部分。"
      },
      {
          "value": "2",
          "text": "边框、网格是基本组成中的图形部分。"
      },
      {
          "value": "3",
          "text": "数据图形（折线图及散点图）是基本组成中的图形部分。"
      },
  ]
})

quizzes.append({
  "id": "choice-2",
  "type": "SELECT",
  "title": "以下关于 matplotlib 绘制图形的层次的说法，错误的是：",
  "answer": "3",
  "options": [
      {
          "value": "0",
          "text": "画架层（canvas）类似于在绘画时需要一个画架放置画板。"
      },
      {
          "value": "1",
          "text": "画板层（figure）是指在画板上可以铺上画纸，是允许绘图的最大空间"
      },
      {
          "value": "2",
          "text": "画纸层（axes）上可以进行各种图形的绘制，图形的组成元素在画纸上体现"
      },
      {
          "value": "3",
          "text": "画板层（figure）可以包含一张画纸绘制单个图，但是无法包含多张画纸绘制多个子图或者图中图。"
      },
  ]
})

ipyquiz.QuizWidget(value=quizzes, type=type, quiz_id="__ipyquiz_quiz_id")
`;

const addQuizStep = function () {
  insertMarkdownCellBelow('### 步骤标题');

  insertCodeCellBelow(`#platform-desc
from ipyaliplayer import Player
Player(vid='--替换你的视频id，上传地址 https://www.boyuai.com/elites/admin/public-video', aspect_ratio=4/3)
`);

  insertMarkdownCellBelow(`<!--步骤描述 -->

#### 知识点
- 总结视频中的知识点`);
  insertCodeCellBelow(quizString);
};

const addUploadFileStep = function () {
  insertMarkdownCellBelow('### 步骤标题');

  insertCodeCellBelow(`#platform-desc
from ipyaliplayer import Player
Player(vid='--替换你的视频id，上传地址 https://www.boyuai.com/elites/admin/public-video', aspect_ratio=4/3)
`);

  insertMarkdownCellBelow(`<!--步骤描述 -->

#### 知识点
- 总结视频中的知识点`);

  insertCodeCellBelow(`#platform-upload-file
[
  {
      "file-type": "image",
      "file-max-count": 1,
      "title": "请上传一张图片"
  },
  {
      "file-type": "doc",
      "file-max-count": 2,
      "title": "请上传全部的文本文件"
  }
]`);
};

const addSummary = function () {
  insertCodeCellBelow(`#platform-summary

`);
  insertMarkdownCellBelow(`
题解部分

<!-- ---------------------------------------- -->
<!-- /////////// 视频播放器 Begin /////////// -->
<!-- ---------------------------------------- -->
<div class="ipy-ali-player" data-vid="【此处填入视频vid】" data-aspect-ratio="4/3"></div>
<!-- ---------------------------------------- -->
<!-- /////////// 视频播放器 End //////////// -->
<!-- ---------------------------------------- -->
`);
};

const addDetailStep = function () {
  insertCodeInCurrentMarkdownCell(`
<details>

<summary>标题</summary>

内容

</details>
  `);
};

const addImagePlayerStep = function () {
  insertCodeInCurrentMarkdownCell(`
<!-- ---------------------------------------- -->
<!-- /////////// 图片播放器 Begin /////////// -->
<!-- ---------------------------------------- -->
<div class="image-player">
<div class="image-viewer">


<!-------------- 在此处添加图片资源 ------------------->
<img src="【在此处粘贴替换图片地址】" />
<img src="【在此处粘贴替换图片地址】" />
<img src="【在此处粘贴替换图片地址】" />
<!-------------- 在此处添加图片资源 ------------------->


</div>
<div class="button-wrapper">
<button class="last"></button>
<div>
<span class="current">0</span>
<span>/</span>
<span class="total">0</span>
</div>
<button class="next"></button>
</div>
</div>
<!-- ---------------------------------------- -->
<!-- /////////// 图片播放器 End //////////// -->
<!-- ---------------------------------------- -->
`);
};

const addVideoPlayerStep = function () {
  insertCodeInCurrentMarkdownCell(`
<!-- ---------------------------------------- -->
<!-- /////////// 视频播放器 Begin /////////// -->
<!-- ---------------------------------------- -->
<div class="ipy-ali-player" data-vid="【此处填入视频vid】" data-aspect-ratio="4/3"></div>
<!-- ---------------------------------------- -->
<!-- /////////// 视频播放器 End //////////// -->
<!-- ---------------------------------------- -->
`);
};

const addAudioStep = function () {
  insertCodeInCurrentMarkdownCell(`
<!-- ---------------------------------------- -->
<!-- /////////// 音频播放器 Begin /////////// -->
<!-- ---------------------------------------- -->
<audio controls>
  <source src="【此处填入音频链接】" />
</audio>
<!-- ---------------------------------------- -->
<!-- /////////// 音频播放器 End //////////// -->
<!-- ---------------------------------------- -->
`);
};

const addUserSelectNoneCode = function() {
  insertCodeInCurrentMarkdownCell(`
<div style="user-select:none;">

\`\`\`
// insert something...
\`\`\`

</div>
`);
}

const addFileCell = function () {
  insertCodeCellBelow(`#platform-lock-hidden

import os
# basepath与惠楚确认
basepath = os.path.expanduser('~/share/bby/')

# 以下2选1, 请阅读博小鱼对接文档
#os.chdir(basepath)
#filepath = os.path.join(basepath, 'test.txt')`);
};

const syncLesson = async function () {
  // 注意这边导出了 JSON，所以下面怎么改都和原对象无关，如果同步时修改了数据，重开才能读到
  const content = Jupyter.notebook.toJSON();

  const pathRegRes = workRegx.exec(Jupyter.notebook.notebook_path);
  const baseRegRes = /user\/(dev-)?user-(\d+)/.exec(Jupyter.notebook.base_url);
  if (!pathRegRes || !baseRegRes) {
    alert('工作路径匹配失败');
    return;
  }
  const isDev = baseRegRes[1] === 'dev-';
  const domain = isDev ? 'dev.boyuai.com' : 'www.boyuai.com';
  const lessonId = Number(pathRegRes[1]);
  const token = pathRegRes[2];
  const apiPrefix = `https://${domain}/api/v1`;
  const userId = Number(baseRegRes[2]);

  // const lessonId = 1;
  // const token = 'invalidtoken';
  // const apiPrefix = 'http://localhost:3000';
  // const userId = 5751;

  const _sync = async () => {
    const body = {
      content,
      userId,
      token,
    };
    const path = `${apiPrefix}/lessons/${lessonId}/jupyter`;
    fetch(`${path}`, {
      body: JSON.stringify(body),
      headers: {
        'content-type': 'application/json',
      },
      method: 'PUT',
    })
      .then((response) => {
        if (response.ok) {
          alert('同步成功，请刷新博小鱼步骤页后查看，中途请不要运行代码');
        } else {
          response.json().then((res) => {
            const reason = res.message || res.error || '原因未知';
            alert('同步失败, ' + reason);
          });
        }
      })
      .catch((err) => {
        console.error(err);
      });
  };

  try {
    // 校验 jupyter 格式
    const steps = parseStepsFromCells(content as any);

    // 检查是否预留verify块
    for (let i = 0; i < steps.length; i++) {
      const step = steps[i];
      if (
        (step as any).stepType === 'code' &&
        step.verify === '' &&
        !(step as any).verifyCode
      ) {
        let lastCodeCell =
          step.codeAnswerCells[step.codeAnswerCells.length - 1];
        if (
          !lastCodeCell ||
          lastCodeCell.$cellIndex! <
            step.codeCells[step.codeCells.length - 1].$cellIndex!
        ) {
          lastCodeCell = step.codeCells[step.codeCells.length - 1];
        }
        if (!lastCodeCell) {
          throw new BBYError(`代码题步骤 ${step.title} 的 Code cell 不合法`);
        }
        const nextCell = content.cells[(lastCodeCell.$cellIndex || 0) + 1];
        const nextCellIsEmptyVerify =
          nextCell &&
          nextCell.cell_type === 'markdown' &&
          nextCell.source === '';
        if (!nextCellIsEmptyVerify) {
          throw new BBYError(
            `代码题步骤 ${step.title} 没有正确预留verify块`,
            lastCodeCell.$cellIndex,
            `cellIndex ${lastCodeCell.$cellIndex || 0}`
          );
        }
      }
    }

    // 清理垃圾 & 冗余数据
    for (let cellIndex = 0; cellIndex < content.cells.length; cellIndex++) {
      const c: ICell = content.cells[cellIndex];

      // 清理运行数据
      if (c.outputs) {
        c.outputs = [];
        c.execution_count = null;
      }

      // 清空非配置字段，避免影响用户数据
      Object.keys(c.metadata).forEach((key) => {
        if (!key.startsWith('bxy')) {
          delete (c.metadata as any)[key];
        }
      });

      // 检查是否预留了视频cell
      if (c.cell_type === 'markdown' && c.source.indexOf('### ') === 0) {
        const nextIsDescCode =
          content.cells[cellIndex + 1] &&
          content.cells[cellIndex + 1].source.indexOf('#platform-desc') == 0;
        if (!nextIsDescCode) {
          throw new BBYError(
            `步骤 ${c.source.replace('###', '')} 没有预留视频块`,
            cellIndex,
            `cellIndex: ${cellIndex}

模板：
#platform-desc
# from ipyaliplayer import Player
# Player(vid='替换视频ID', aspect_ratio=4/3)`
          );
        }
      }

      // 解析 Python Quiz Cell，未来会向 JSON 配置方向迁移，抛弃 Python 写法
      const { type, code } = parseCodeCell(c.source);

      if (type === 'quiz') {
        const quizJSON = await parseQuizQuestions({
          code,
          userId,
          lessonId,
          token,
          apiPrefix,
        });
        // console.log('quiz 解析结果', { quizJSON });

        if (quizJSON?.statusCode) {
          throw new BBYError(
            `Quiz 解析失败: ${quizJSON?.message}`,
            cellIndex,
            code
          );
        }

        if (!quizJSON.value || !quizJSON.value.length) {
          throw new BBYError('Quiz 解析失败: 缺少选项', cellIndex);
        }

        for (const question of quizJSON.value) {
          // 如果题目来自题库，获取当前最新数据
          if (
            typeof question.id === 'string' &&
            question.id.startsWith('uuid-')
          ) {
            const uuid = question.id.slice(5);
            const questionJSON = await getQuizQuestionByUUID({
              uuid,
              apiPrefix,
            });
            // console.log('来自题库的 quiz question', { questionJSON });
            if (!questionJSON.uuid) {
              throw new BBYError(
                `Quiz 解析失败: 题目 ${question.id} 解析异常`,
                cellIndex
              );
            }
            const questionIndex = quizJSON.value.findIndex(
              (option: IQuestion) => option.id === question.id
            );
            if (questionIndex === -1) {
              throw new BBYError(
                `Quiz 解析失败: 题目 ${question.id} 匹配失败`,
                cellIndex
              );
            }
            // console.log('开始更新 quiz quetion', {
            //   questionWIP: quizJSON.value[questionIndex],
            // });
            const options = parseQuestionOptions(questionJSON);
            quizJSON.value[questionIndex] = {
              ...questionJSON,
              id: question.id,
              options,
            };
            console.log('quiz quetion 更新完成', {
              question: quizJSON.value[questionIndex],
            });
          }

          // 冗余 quiz 数据
          if (!c.metadata.bxyQuizStep) {
            c.metadata.bxyQuizStep = {};
          }
          c.metadata.bxyQuizStep.json = quizJSON;
        }
      }
    }
    // 同步
    _sync();
  } catch (error: any) {
    Jupyter.dialog.modal({
      title: '可能存在错误，请确认是否同步',
      body:
        `<p style="margin-bottom: 8px">${error?.message || '未知错误'}</p>` +
        `<pre>${error?.detail || JSON.stringify(error)}</pre>`,
      sanitize: false,
      buttons: {
        强行同步: {
          click: _sync,
        },
        [error.cellIndex != null ? '取消同步，查看错误Cell' : '取消同步']: {
          class: 'btn-primary',
          click: () => {
            if (error.cellIndex != null) {
              Jupyter.notebook.select(error.cellIndex);
              Jupyter.notebook.focus_cell();
            }
          },
        },
      },
    });
  }
};
