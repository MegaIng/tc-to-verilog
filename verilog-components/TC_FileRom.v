module TC_FileRom (clk, rst, en, address, out);
    parameter MEM_BYTES = 65536;
    parameter HEX_FILE = "test_jumps.mem";
    parameter ARG_SIG = "HEXFILE=%s";
    parameter FILE_BYTES = 755;
    reg [1024*8:0] hexfile;
    integer filebytes;
    input clk;
    input rst;
    input en;
    input [63:0] address;
    output reg [63:0] out;

    reg [7:0] mem [0:MEM_BYTES];
    integer fid;
    integer fsize;
    integer data;

    initial begin
        hexfile = HEX_FILE;
        filebytes = FILE_BYTES;

        if ($value$plusargs(ARG_SIG, hexfile)) begin
            $display("loading %0s", hexfile);
            $readmemh(hexfile, mem);
        end

        //fid = $fopen(hexfile, "rb");
        //if (fid == 0) begin
        //    $display("cannot open file");
        //    $stop;
        //end
        //fsize = $fseek(fid, 0, 2);
        //if (fsize == -1) begin
        //    $display("cannot move file pointer");
        //    $stop;
        //end
        //fsize = $ftell(fid);
        //$display("file is %0d bytes", fsize); 
        //$fseek(fid, 0, 0);
        //data = $fread(fid, mem[0]);
        //$display("read %0d vectors\n", data);
        //data = $fcloser(fid);
        //$fclose(fid);
    end

    always @ (posedge clk or posedge rst) begin
        if (rst || !en) begin
            out = {64{1'b0}};
        end else if (address == {64{1'b1}}) begin
            out = filebytes;
        end else begin
            out[7:0] = mem[address];
            out[15:8] = mem[address+1];
            out[23:16] = mem[address+2];
            out[31:24] = mem[address+3];
            out[39:32] = mem[address+4];
            out[47:40] = mem[address+5];
            out[55:48] = mem[address+6];
            out[63:56] = mem[address+7];
        end
    end
endmodule

