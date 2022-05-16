module TC_FileRom (clk, rst, en, address, out);
    parameter UUID = 0;
    parameter NAME = "";
    parameter BIT_WIDTH = 8;
    parameter BIT_DEPTH = 302;
    parameter HEX_FILE = "test_jumps.mem";
    parameter ARG_SIG = "HEX_FILE=%s";
//    parameter FILE_BYTES = 302;
    integer filebytes;
    reg [1024*8:0] hexfile;
    
    input clk;
    input rst;
    input en;
    input [63:0] address;
    output reg [63:0] out;

    reg [BIT_WIDTH:0] mem [0:BIT_DEPTH];
    integer fd;
    integer fsize;
    integer data;
    integer i;
    
    initial begin
        hexfile = HEX_FILE;
        filebytes = BIT_DEPTH;

        i = ($value$plusargs(ARG_SIG, hexfile));
        $display("loading %0s", hexfile);
        fd = $fopen(hexfile, "r");
        if (fd) begin
            i = 0;
            while (!$feof(fd) && i < BIT_DEPTH) begin
                mem[i] = $fgetc(fd);
                i = i + 1;
            end
            $display("read %0d bytes", i);
        end else begin
            $display("file not found");
        end
        $fclose(fd);
        out = {64{1'b0}};

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

    always @ (address or en or rst) begin
        if (rst || !en) begin
            out = {64{1'b0}};
        end else if (address == {64{1'b1}}) begin
            out = filebytes;
        end else begin
            if (address < BIT_DEPTH)
                out[7:0] = mem[address];
            else
                out[7:0] = {8{1'b0}};
            if (address+1 < BIT_DEPTH)
                out[15:8] = mem[address+1];
            else
                out[15:8] = {8{1'b0}};
            if (address+2 < BIT_DEPTH)
                out[23:16] = mem[address+2];
            else
                out[23:16] = {8{1'b0}};
            if (address+3 < BIT_DEPTH)
                out[31:24] = mem[address+3];
            else
                out[31:24] = {8{1'b0}};
            if (address+4 < BIT_DEPTH)
                out[39:32] = mem[address+4];
            else
                out[39:32] = {8{1'b0}};
            if (address+5 < BIT_DEPTH)
                out[47:40] = mem[address+5];
            else
                out[47:40] = {8{1'b0}};
            if (address+6 < BIT_DEPTH)
                out[55:48] = mem[address+6];
            else
                out[55:48] = {8{1'b0}};
            if (address+7 < BIT_DEPTH)
                out[63:56] = mem[address+7];
            else
                out[63:56] = {8{1'b0}};
        end
    end
endmodule

