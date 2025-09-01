document.addEventListener('DOMContentLoaded', () => {
    const startChatBtn = document.getElementById('start-chat-btn');
    const chatBox = document.getElementById('chat-box');
    const loader = document.getElementById('loader');

    // バックエンドAPIのエンドポイント
    const API_ENDPOINT = '/api/gemini/generate';

    /**
     * バックエンドAPIへリクエストを送信する非同期関数
     * この関数はシミュレーションのため、そのまま使用します。
     */
    async function callGeminiApi(model, prompt, delay) {
        // ...（この関数の中身は変更ありません）
        console.log(`[リクエスト送信] モデル: ${model}, プロンプト: "${prompt}"`);
        return new Promise(resolve => {
            setTimeout(() => {
                const responseText = `"${prompt}" に応えて、最高の挨拶をします！ こんにちは！`;
                console.log(`[レスポンス受信] モデル: ${model}`);
                resolve(`[${model}からの返信]: ${responseText}`);
            }, delay);
        });
    }

    /**
     * チャット開始ボタンがクリックされたときの処理
     */
    startChatBtn.addEventListener('click', async () => {
        // UIを処理開始状態に更新
        chatBox.value = '';
        loader.classList.remove('hidden');
        startChatBtn.disabled = true;
        chatBox.placeholder = "Geminiからの返信を待っています...";

        try {
            // --- 1. 全てのリクエストを並行して開始 ---
            const promise1 = callGeminiApi('gemini-1.5-flash-lite', 'あいさつを返す', 1000);
            const promise2 = callGeminiApi('gemini-1.5-flash', 'あいさつを返す', 2000); // 遅延を少し調整して動作を確認しやすくします
            const promise3 = callGeminiApi('gemini-1.5-flash', '最高の挨拶を考えて返す', 3000);

            // --- 2. 全てのリクエストが完了するまで待機 ---
            // Promise.allSettled は、いずれかが失敗しても全ての完了を待つため、エラー耐性が高いです。
            const results = await Promise.allSettled([promise1, promise2, promise3]);

            // --- 3. 全てのデータが揃ってから、UIを更新 ---
            // これによりエラー処理がシンプルになり、意図せず処理が止まることを防ぎます。

            // リクエスト1の結果を処理
            if (results[0].status === 'fulfilled') {
                chatBox.value += `✅ [速いモデルからの最初の返信]\n${results[0].value}\n\n`;
            } else {
                console.error('Promise 1 failed:', results[0].reason);
                chatBox.value += `❌ [速いモデルからの返信でエラーが発生しました]\n\n`;
            }

            // リクエスト2と3の結果を処理
            const response2 = results[1];
            const response3 = results[2];
            
            // 両方が成功した場合
            if (response2.status === 'fulfilled' && response3.status === 'fulfilled') {
                chatBox.value += `✅ [標準モデルからの返信 (2件)]\n- ${response2.value}\n- ${response3.value}\n\n`;
            } else {
                // どちらか、または両方が失敗した場合
                chatBox.value += `⚠️ [標準モデルからの返信に問題がありました]\n`;
                if (response2.status === 'rejected') {
                    console.error('Promise 2 failed:', response2.reason);
                }
                 if (response3.status === 'rejected') {
                    console.error('Promise 3 failed:', response3.reason);
                }
            }

        } catch (error) {
            // このcatchは、await Promise.allSettled 自体のエラーなど、予期せぬ重大なエラーを捕捉します
            console.error('チャット処理中に予期せぬエラーが発生しました:', error);
            chatBox.value += 'エラーが発生しました。詳細はコンソールを確認してください。';
        } finally {
            // このブロックは try 内の処理が成功しようと失敗しようと、必ず最後に実行されます
            loader.classList.add('hidden');
            startChatBtn.disabled = false;
            chatBox.placeholder = "ここにGeminiからの返信が表示されます...";
        }
    });
});