from fipper.viper import Viper

class LeaveVoiceCall(Viper):
    async def _leave_voice_call(
        self,
        params: dict,
    ):
        result = {
            'result': 'OK',
        }
        try:
            await self.assistant.leave_group_call(
                int(params['chat_id']),
            )
        except Exception as e:
            result = {
                'result': str(e),
            }
        return result
