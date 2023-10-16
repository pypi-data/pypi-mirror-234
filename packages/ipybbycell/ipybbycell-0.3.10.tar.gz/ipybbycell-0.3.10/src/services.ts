export const parseQuizQuestions = async ({
  code,
  lessonId,
  userId,
  token,
  apiPrefix,
}: {
  code: string;
  lessonId: number;
  userId: number;
  token: string;
  apiPrefix: string;
}): Promise<any> => {
  const body = {
    code,
    lessonId,
    userId,
    token,
  };
  return fetch(`${apiPrefix}/jupyterhub/admin-widgets-parse/json`, {
    body: JSON.stringify(body),
    headers: {
      'content-type': 'application/json',
    },
    method: 'POST',
  }).then((response) => {
    return response.json();
  });
};

export const getQuizQuestionByUUID = async ({
  uuid,
  apiPrefix,
}: {
  uuid: string;
  apiPrefix: string;
}): Promise<any> => {
  return fetch(`${apiPrefix}/quiz-questions/uuid/${uuid}`, {
    headers: {
      'content-type': 'application/json',
    },
    method: 'GET',
  }).then((response) => {
    return response.json();
  });
};
