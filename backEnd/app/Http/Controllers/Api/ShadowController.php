<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use Symfony\Component\Process\Process;

class ShadowController extends Controller
{
    public function search($user)
    {
        if ($user) {
            try {
                $pythonScriptPath = base_path() . '/python/script.py';
                $process = new Process(['python3', $pythonScriptPath, $user]);
                $process->run();
                if (!$process->isSuccessful()) {
                    return [
                        'status' => 'failed',
                        'error' => 1100,
                        'user_state' => null,
                        'data' => "process failed"
                    ];
                }
                $output = json_decode($process->getOutput());
            } catch (\Exception $e) {
                return [
                    'status' => 'failed',
                    'error' => 1100,
                    'user_state' => null,
                    'data' => $e->getMessage()
                ];
            }
            return $output;
        } else {
            return [
                'status' => 'success',
                'error' => null,
                'user_state' => 3,
                'data' => null
            ];
        }
    }
}
